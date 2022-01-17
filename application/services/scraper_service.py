from datetime import datetime, timedelta
from typing import List, Optional, Tuple
import urllib
import pytz
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.elements import and_
from sqlalchemy.sql.expression import or_
from application import models, db
from werkzeug.exceptions import NotFound, BadRequest


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

    def _get_url(self, url):
        try:
            return requests.get(url)
        except requests.exceptions.MissingSchema:
            raise BadRequest(
                f"The url {url} is missing a schema. \nDid you forget https:// ?"
            )
        except requests.exceptions.HTTPError:
            raise NotFound(
                f"The url {url} has an error. \nPlease confirm the link exists!"
            )
        except requests.exceptions.ConnectionError:
            raise NotFound(f"Couldn't connect to {url}. \nDoes it exist?")
        except Exception:
            raise BadRequest(
                f"Couldn't read {url}. \nIf the problem persists, remove this url from the search."
            )

    def _scrape(self, site: str, link: str):
        res = self._get_url(link)
        parsed_url = urllib.parse.urlparse(link)
        base_url = f"{parsed_url[0]}://{parsed_url[1]}"
        if res.status_code != 200:
            print(f"Error {res.status_code}: {link}")
            yield None
        soup = BeautifulSoup(res.text, "html.parser")
        list_of_links = soup.select("a")
        previous_urls = set()
        for item in list_of_links:
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

    def _upsert_results(self, results: List[dict]):
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
        return q.all()

    def _get_today_start_end_time(self) -> Tuple[datetime, datetime]:
        tz = pytz.timezone("America/Toronto")
        now = pytz.utc.localize(datetime.utcnow()).astimezone(tz)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        return start, end

    def scrape_sites(self, include_previous: bool) -> List[models.Result]:
        all_results = []
        for location in self.search.search_locations:
            for results in self._scrape(location.name, location.url):
                if not results:
                    continue
                all_results.append(results)
        self._upsert_results(all_results)
        start, end = self._get_today_start_end_time()
        return self.get_results(start, end, include_previous)

    def scrape_all(self, include_previous: bool) -> List[models.Result]:
        self.search.search_locations
        potential_links = []

        for location in self.search.search_locations:
            site = location.name
            link = location.url
            res = res = self._get_url(link)
            soup = BeautifulSoup(res.content, features="xml")
            parsed_url = urllib.parse.urlparse(link)
            base_url = f"{parsed_url[0]}://{parsed_url[1]}"
            list_of_links = soup.findAll("item")
            for item in list_of_links:
                try:
                    if "http" in item.link.text:
                        potential_links.append(
                            {
                                "agency": site,
                                "title": item.title.text.strip().split("\n")[0],
                                "link": item.link.text,
                                "search_id": self.search.id,
                            }
                        )
                    else:
                        relative_path = item.link.text
                        complete_url = f"{base_url}{relative_path}"
                        potential_links.append(
                            {
                                "agency": site,
                                "title": item.title.text.strip().split("\n")[0],
                                "link": complete_url,
                                "search_id": self.search.id,
                            }
                        )
                except:
                    print("Error Found!")
        self._upsert_results(potential_links)
        start, end = self._get_today_start_end_time()
        return self.get_results(start, end, include_previous)
