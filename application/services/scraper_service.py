from datetime import datetime, timedelta
from typing import List, Optional
import urllib
import pytz
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.elements import and_
from sqlalchemy.sql.expression import or_
from sqlalchemy.sql.functions import mode
from application import models, db
from flask import jsonify


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

    def _scrape(self, site: str, link: str):
        res = requests.get(link)
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
            if url in previous_urls:
                continue
            if any(term in item.text.lower() for term in self.terms):
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
        q = models.Result.query
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

    def scrape_sites(self, include_previous: bool) -> List[models.Result]:
        all_results = []
        for location in self.search.search_locations:
            for results in self._scrape(location.name, location.url):
                if not results:
                    continue
                all_results.append(results)
        self._upsert_results(all_results)
        tz = pytz.timezone("America/Toronto")
        now = pytz.utc.localize(datetime.utcnow()).astimezone(tz)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        return self.get_results(start, end, include_previous)
