from extensions import db

from flask import Blueprint, jsonify, request
from datetime import datetime
from sqlalchemy import extract

from ..employees import Employee
from .models import ShiftRequest
from .schemas import shift_request_schema

shifts_requests_bp = Blueprint('shifts_requests', __name__)


# 特定の月のシフト希望取得
@shifts_requests_bp.route('/<int:year>/<int:month>', methods=['GET'])
def get_shift_requests_for_month(year, month):
    # 指定された年と月のシフト希望を取得
    shift_requests = ShiftRequest.query.filter(
        extract('year', ShiftRequest.date) == year,
        extract('month', ShiftRequest.date) == month
    ).all()

    # シフト希望データのシリアライズ（または適切な形式への変換）が必要
    shift_requests_data = [{'id': sr.id, 'employee_id': sr.employee_id, 'date': sr.date.strftime(
        '%Y-%m-%d'), 'type_of_vacation': sr.type_of_vacation} for sr in shift_requests]

    return jsonify(shift_requests_data)


# 希望シフト追加
@shifts_requests_bp.route('/', methods=['POST'])
def add_or_update_shift_requests():
    requests_data = request.json

    # 全てのシフト希望に対してバリデーションを実施
    errors = shift_request_schema.validate(requests_data, many=True)
    if errors:
        return jsonify(errors), 400

    # 各シフト希望に対する処理
    for data in requests_data:
        employee_id = data['employee_id']
        shift_date = datetime.strptime(data['date'], '%Y-%m-%d')
        type_of_vacation = data['type_of_vacation']

        employee = Employee.query.get(employee_id)
        if not employee:
            continue  # 従業員が見つからない場合はスキップ

        shift_request = ShiftRequest.query.filter_by(
            employee_id=employee_id, date=shift_date).first()

        if shift_request:
            shift_request.type_of_vacation = type_of_vacation
        else:
            new_request = ShiftRequest(
                employee_id=employee_id,
                date=shift_date,
                type_of_vacation=type_of_vacation
            )
            db.session.add(new_request)

    db.session.commit()
    return jsonify({"message": "Shift requests updated successfully"}), 200


# 希望シフト削除
@shifts_requests_bp.route('/<int:request_id>', methods=['DELETE'])
def delete_shift_request(request_id):
    shift_request = ShiftRequest.query.get(request_id)

    if not shift_request:
        return jsonify({"message": "Shift request not found"}), 404

    db.session.delete(shift_request)
    db.session.commit()
    return jsonify({"message": "Shift request deleted successfully"}), 200
