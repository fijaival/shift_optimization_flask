
from flask import Blueprint, jsonify, request
from .services.data_fetcher import fetch_restrictions

shift_generation_bp = Blueprint('shift_generation', __name__)


@shift_generation_bp.route('/', methods=["GET"])
def employees():
    test = fetch_restrictions()
    return test
