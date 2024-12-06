# routes.py
from flask import Blueprint

bp = Blueprint("main", __name__)


@bp.route("/test", methods=["GET"])
def test():
    return "success"
