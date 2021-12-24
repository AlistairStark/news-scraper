from datetime import datetime
import os
from typing import List
from flask import send_file
from application import models
import tempfile
import csv
from werkzeug.exceptions import NotFound


class DownloadService(object):
    def _get_results_by_ids(self, ids: List[int]) -> List[models.Result]:
        return models.Result.query.filter(models.Result.id.in_(ids)).all()

    def _get_search_name(self, search_id: int) -> str:
        search: models.Search = models.Search.query.get(search_id)
        if not search:
            raise NotFound("Search not found")
        return search.name

    def download_csv(self, ids: List[int], search_id: int):
        results = self._get_results_by_ids(ids)
        name = self._get_search_name(search_id)
        date = datetime.now().date()
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f"{name}-{date}.csv")
            with open(filename, "w") as f:
                writer = csv.DictWriter(f, ["Agency", "Title", "Link"])
                for r in results:
                    row = {"Agency": r.agency, "Title": r.title, "Link": r.link}
                    writer.writerow(row)
            return send_file(filename, mimetype="text/csv", as_attachment=True)
