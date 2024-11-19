from flask import Blueprint, jsonify, request

bp = Blueprint("main", __name__)


@bp.route("/test", methods=["GET"])
def test():
    return "success"
