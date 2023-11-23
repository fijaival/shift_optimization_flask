
from flask import Blueprint, jsonify, request
from .services.optimizer import totake

shift_generation_bp = Blueprint('shift_generation', __name__)


@shift_generation_bp.route('/', methods=["GET"])
def employees():
    test = totake()
    return test
