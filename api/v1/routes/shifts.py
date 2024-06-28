from flask import Blueprint, request, jsonify
from extensions import self_facility_required
from api.v1.utils.error import InvalidAPIUsage
from ..service.scheduler.run_optimization import run_optimization
from ..service.shift import post_shifts_service, get_shifts_service
shifts_bp = Blueprint("shift", __name__)


@shifts_bp.route('/facilities/<int:facility_id>/shifts/generate', methods=['POST'])
@self_facility_required
def generate_shift(facility_id):
    year = request.args.get('year')
    month = request.args.get('month')
    res: list = run_optimization(facility_id, year, month)
    if not res:
        raise InvalidAPIUsage("Facility not found", 404)
    return jsonify({"shifts": res}), 200


@shifts_bp.route('/facilities/<int:facility_id>/shifts', methods=['GET'])
@self_facility_required
def get_shifts(facility_id):
    year = request.args.get('year')
    month = request.args.get('month')
    res = get_shifts_service(facility_id, year, month)
    if not res:
        raise InvalidAPIUsage("shifts not found", 404)
    return jsonify({"shifts": res}), 200


@shifts_bp.route('/facilities/<int:facility_id>/shifts', methods=['POST'])
@self_facility_required
def confirm_shift(facility_id):
    data = request.json
    post_shifts_service(data)
    return jsonify({"message": "Shifts confirmed successfully!"}), 200
