from flask import Blueprint, request
from extensions import self_facility_required
from api.v1.utils.error import InvalidAPIUsage
from ..service.scheduler.run_optimization import run_optimization

shifts_bp = Blueprint("shift", __name__)

# 自動生成処理未実装


@shifts_bp.route('/facilities/<int:facility_id>/shifts', methods=['POST'])
@self_facility_required
def confirm_shift():
    pass


@shifts_bp.route('/facilities/<int:facility_id>/shifts/generate', methods=['POST'])
@self_facility_required
def generate_shift(facility_id):
    year = request.args.get('year')
    month = request.args.get('month')
    res = run_optimization(facility_id, year, month)
    if not res:
        raise InvalidAPIUsage("Facility not found", 404)
    return res, 200
