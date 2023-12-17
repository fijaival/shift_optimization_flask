
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from .optimizer import optimize

shift_generation_bp = Blueprint('shift_generation', __name__)


@shift_generation_bp.route('/<int:year>/<int:month>', methods=["GET"])
@jwt_required()
def get_shift(year, month):
    holiday_set = request.args.get('holiday_set')

    if holiday_set is None:
        return jsonify({'error': 'Missing required parameter: holiday_set'}), 400

    try:
        holiday_set = int(holiday_set)
    except ValueError:
        return jsonify({'error': 'Invalid value for holiday_set, must be an integer'}), 400
    test = optimize(year, month, holiday_set)
    return test
