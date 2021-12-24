from flask_restful import Api

from application.api.v1.user_controller import CreateUser, LoginUser
from application.api.v1.search_controller import (
    Search,
    SearchTerms,
    SearchLocations,
    SearchAll,
)
from application.api.v1.scrape_controller import Scrape
from application.api.v1.download_controller import DownloadCsv


def init_routes(app: Api):
    app.add_resource(CreateUser, "/v1/user/create")
    app.add_resource(LoginUser, "/v1/user/login")
    app.add_resource(Search, "/v1/search")
    app.add_resource(SearchAll, "/v1/search-all")
    app.add_resource(SearchTerms, "/v1/search-terms")
    app.add_resource(SearchLocations, "/v1/search-location")
    app.add_resource(Scrape, "/v1/scrape")
    app.add_resource(DownloadCsv, "/v1/download-csv")
