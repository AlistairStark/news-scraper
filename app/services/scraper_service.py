import asyncio
import logging
import urllib
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import httpx
import pytz
from bs4 import BeautifulSoup
from bs4.element import Tag
from app.models.schema import Result, Search, SearchLocation

from app.repositories.result_repository import ResultRepository

logger = logging.getLogger(__name__)


class ScraperService:
    def __init__(self, db_session, search: Search):
        self.result_repository = ResultRepository(db_session)
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

    def _scrape_feed(self, site: str, link: str, res) -> List[Result]:
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

    async def scrape_sites(self, include_previous: bool) -> List[Result]:
        all_results = []
        links_set = set()
        for locations in self._chunks(self.search.search_locations):
            async with httpx.AsyncClient() as session:
                responses = await asyncio.gather(
                    *[self._get_page(session, l) for l in locations],
                    return_exceptions=False,
                )
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
        await self.result_repository.upsert_results(all_results)
        start, end = self._get_today_start_end_time()
        return await self.result_repository.get_results(
            self.search.id,
            start,
            end,
            include_previous,
        )
