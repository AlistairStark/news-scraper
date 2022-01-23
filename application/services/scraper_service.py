import asyncio
import logging
import urllib
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import httpx
import pytz
from bs4 import BeautifulSoup
from bs4.element import Tag
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.elements import and_
from sqlalchemy.sql.expression import or_

from application import db, models
from application.models.schema import SearchLocation

logger = logging.getLogger(__name__)


class ScraperService(object):
    def __init__(self, search: models.Search):
        self.search = search
        self.terms = [t.term.lower() for t in search.search_terms]

    def _get_url(self, item: Tag, base_url: str) -> Optional[str]:
        complete_url = item.get("href")
        if item.get("href") and not "http" in item.get("href"):
            relative_path = item["href"]
            complete_url = f"{base_url}{relative_path}"
        return complete_url

    def _chunks(self, main_list, chunk_size=10):
        for i in range(0, len(main_list), chunk_size):
            yield main_list[i : i + chunk_size]

    def _get_today_start_end_time(self) -> Tuple[datetime, datetime]:
        tz = pytz.timezone("America/Toronto")
        now = pytz.utc.localize(datetime.utcnow()).astimezone(tz)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        return start, end

    def _validate_result(self, result: dict) -> bool:
        return (
            result.get("agency")
            and result.get("title")
            and result.get("link")
            and result.get("search_id")
        )

    async def _get_page(self, session: httpx.AsyncClient, location: SearchLocation):
        try:
            logger.info(f"STARTING SCRAPE: {location.url}")
            res = await session.get(location.url)
            res.raise_for_status()
            logger.info(f"ENDING SCRAPE: {location.url}")
            if self.search.is_rss:
                return [
                    scrape
                    for scrape in self._scrape_feed(location.name, location.url, res)
                ]
            return [scrape for scrape in self._scrape(location.name, location.url, res)]
        except httpx.ConnectError as e:
            logger.error(f"ConnectError scraping page {location.url}: {e}")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTPStatusError scraping page {location.url}: {e}")
        except httpx.RequestError as e:
            logger.error(f"RequestError scraping page {location.url}: {e}")
        except Exception as e:
            logger.error(f"Uncaught error scraping page {location.url}: {e}")

    def _scrape(self, site: str, link: str, res):
        parsed_url = urllib.parse.urlparse(link)
        base_url = f"{parsed_url[0]}://{parsed_url[1]}"
        soup = BeautifulSoup(res.text, "html.parser")
        list_of_links = soup.select("a")
        previous_urls = set()
        for item in list_of_links:
            try:
                url = self._get_url(item, base_url)
                if not url or url in previous_urls:
                    continue
                if len(self.terms) < 1 or any(
                    term in item.text.lower() for term in self.terms
                ):
                    title = item.text.strip().split("\n")[0]
                    previous_urls.add(url)
                    yield dict(
                        agency=site,
                        title=title,
                        link=url,
                        search_id=self.search.id,
                    )
            except Exception as e:
                logger.error(f"Error while scraping: {e}")

    def _scrape_feed(self, site: str, link: str, res) -> List[models.Result]:
        soup = BeautifulSoup(res.content, features="xml")
        parsed_url = urllib.parse.urlparse(link)
        base_url = f"{parsed_url[0]}://{parsed_url[1]}"
        list_of_links = soup.findAll("item")
        title_set = set()
        link_set = set()
        for item in list_of_links:
            try:
                title = item.title.text.strip().split("\n")[0]
                if title in title_set:
                    logger.info(f"Title {title} already exists!")
                    continue
                title_set.add(title)
                if not title or not site:
                    logger.warn(f"error title: {title}, site: {site}")
                    continue
                link_text = ""
                if "http" in item.link.text:
                    link_text = item.link.text
                else:
                    relative_path = item.link.text
                    link_text = f"{base_url}{relative_path}"
                if link_text in link_set:
                    continue
                link_set.add(link_text)
                yield (
                    {
                        "agency": site,
                        "title": item.title.text.strip().split("\n")[0],
                        "link": link_text,
                        "search_id": self.search.id,
                    }
                )
            except Exception as e:
                logger.warn(f"Error Found: {e}")
                continue

    def _upsert_results(self, results: List[dict]):
        if len(results) < 1:
            return
        insert_results = insert(models.Result).values(results)
        upsert_results = insert_results.on_conflict_do_update(
            constraint="unique_link_search",
            set_={"updated_at": datetime.now()},
        )
        db.session.execute(upsert_results)
        db.session.commit()
        db.session.flush()

    def get_results(
        self,
        start: datetime,
        end: datetime,
        include_previous=False,
    ) -> List[models.Result]:
        q = models.Result.query.filter_by(search_id=self.search.id)
        if include_previous:
            q = q.filter(
                or_(
                    and_(
                        models.Result.updated_at >= start,
                        models.Result.updated_at <= end,
                    ),
                    and_(
                        models.Result.created_at >= start,
                        models.Result.created_at <= end,
                    ),
                )
            )
        else:
            q = q.filter(
                models.Result.created_at >= start,
                models.Result.created_at <= end,
            )
        return q.order_by(models.Result.agency).all()

    async def scrape_sites(self, include_previous: bool) -> List[models.Result]:
        for locations in self._chunks(self.search.search_locations):
            links_set = set()
            all_results = []
            async with httpx.AsyncClient() as session:
                tasks = [self._get_page(session, l) for l in locations]
                responses = await asyncio.gather(*tasks, return_exceptions=False)
                for r in responses:
                    if not r:
                        continue
                    for data in r:
                        if not self._validate_result(data) or data["link"] in links_set:
                            logger.info(f"INVALID SCRAPED DATA: {data}")
                            continue
                        logger.info(f"ADDING SCRAPED DATA: {data}")
                        links_set.add(data["link"])
                        all_results.append(data)
            self._upsert_results(all_results)
        start, end = self._get_today_start_end_time()
        return self.get_results(start, end, include_previous)
