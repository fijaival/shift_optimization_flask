from extensions import db, jwt_required, self_facility_required
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, jsonify, request
from ..service.day_off_requests import get_all_requests_services, post_day_off_request_service

# ------------------------------------------------------

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from datetime import datetime
from sqlalchemy import extract

from ..models import DayOffRequest, DayOffRequestSchema


day_off_requests_bp = Blueprint('day_off_requests', __name__)


@day_off_requests_bp.route('/facilities/<int:facility_id>/requests')
@self_facility_required
def get_all_requests():
    pass


@day_off_requests_bp.route('/facilities/<int:facility_id>/employees/<int:employee_id>/requests', methods=["POST"])
@self_facility_required
def add_request(facility_id, employee_id):
    data = request.json
    res = post_day_off_request_service(facility_id, employee_id, data)
    res = DayOffRequestSchema().dump(res)
    return res, 201


@day_off_requests_bp.route('/facilities/<int:facility_id>/employees/<int:employee_id>/requests/<int:request_id>', methods=["DELETE"])
@self_facility_required
def delete_request(facility_id, employee_id, request_id):
    pass


@day_off_requests_bp.route('/facilities/<int:facility_id>/employees/<int:employee_id>/requests/<int:request_id>', methods=["PUT"])
@self_facility_required
def update_request(facility_id, employee_id, request_id):
    pass
# 特定の月のシフト希望取得


# @shifts_requests_bp.route('/<int:year>/<int:month>', methods=['GET'])
# @jwt_required()
# def get_shift_requests_for_month(year, month):
#     # 指定された年と月のシフト希望を取得
#     shift_requests = DayOffRequest.query.filter(
#         extract('year', DayOffRequest.date) == year,
#         extract('month', DayOffRequest.date) == month
#     ).all()

#     # シフト希望データのシリアライズ（または適切な形式への変換）が必要
#     shift_requests_data = [{'id': sr.id, 'employee_id': sr.employee_id, 'date': sr.date.strftime(
#         '%Y-%m-%d'), 'type_of_vacation': sr.type_of_vacation} for sr in shift_requests]

#     return jsonify(shift_requests_data)


# # 希望シフト追加
# @shifts_requests_bp.route('/', methods=['POST'])
# @jwt_required()
# def add_or_update_shift_requests():
#     requests_data = request.json

#     # 全てのシフト希望に対してバリデーションを実施
#     errors = shift_request_schema.validate(requests_data, many=True)
#     if errors:
#         return jsonify(errors), 400

#     # 各シフト希望に対する処理
#     for data in requests_data:
#         employee_id = data['employee_id']
#         shift_date = datetime.strptime(data['date'], '%Y-%m-%d')
#         type_of_vacation = data['type_of_vacation']

#         employee = Employee.query.get(employee_id)
#         if not employee:
#             continue  # 従業員が見つからない場合はスキップ

#         shift_request = DayOffRequest.query.filter_by(
#             employee_id=employee_id, date=shift_date).first()

#         if shift_request:
#             shift_request.type_of_vacation = type_of_vacation
#         else:
#             new_request = DayOffRequest(
#                 employee_id=employee_id,
#                 date=shift_date,
#                 type_of_vacation=type_of_vacation
#             )
#             db.session.add(new_request)

#     db.session.commit()
#     return jsonify({"message": "Shift requests updated successfully"}), 200


# # 希望シフト削除
# @shifts_requests_bp.route('/<int:request_id>', methods=['DELETE'])
# @jwt_required()
# def delete_shift_request(request_id):
#     shift_request = DayOffRequest.query.get(request_id)

#     if not shift_request:
#         return jsonify({"message": "Shift request not found"}), 404

#     db.session.delete(shift_request)
#     db.session.commit()
#     return jsonify({"message": "Shift request deleted successfully"}), 200
