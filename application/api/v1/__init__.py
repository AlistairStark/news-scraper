from flask import Blueprint

from application.api.v1.download_controller import bp as download_bp
from application.api.v1.scrape_controller import bp as scrape_bp
from application.api.v1.search_controller import bp as search_bp
from application.api.v1.user_controller import bp as user_bp

bp = Blueprint("v1", __name__, url_prefix="/v1")

bp.register_blueprint(scrape_bp)
bp.register_blueprint(download_bp)
bp.register_blueprint(search_bp)
bp.register_blueprint(user_bp)
