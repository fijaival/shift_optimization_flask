from extensions import db

from flask import Blueprint, jsonify, request
from datetime import datetime
from sqlalchemy import extract

from ..employees import Employee
from .models import ShiftRequest

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
def add_or_update_shift_request():
    data = request.json

    # データのバリデーション
    if 'employee_id' not in data or not isinstance(data['employee_id'], int):
        return jsonify({'message': 'Invalid or missing employee_id'}), 400

    if 'date' not in data:
        return jsonify({'message': 'Missing date'}), 400

    try:
        shift_date = datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    if 'type_of_vacation' not in data or data['type_of_vacation'] not in ['有', '公']:
        return jsonify({'message': 'Invalid or missing type_of_vacation'}), 400

    # 従業員が存在するかどうかを確認
    employee = Employee.query.get(data['employee_id'])
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    # 既存のシフト希望の検索と更新、または新しいシフト希望の追加
    shift_request = ShiftRequest.query.filter_by(
        employee_id=data['employee_id'], date=shift_date).first()

    if shift_request:
        shift_request.type_of_vacation = data['type_of_vacation']
    else:
        new_request = ShiftRequest(
            employee_id=data['employee_id'],
            date=shift_date,
            type_of_vacation=data['type_of_vacation']
        )
        db.session.add(new_request)

    db.session.commit()
    return jsonify({"message": "Shift request updated successfully"}), 200


# 希望シフト削除
@shifts_requests_bp.route('/<int:request_id>', methods=['DELETE'])
def delete_shift_request(request_id):
    shift_request = ShiftRequest.query.get(request_id)

    if not shift_request:
        return jsonify({"message": "Shift request not found"}), 404

    db.session.delete(shift_request)
    db.session.commit()
    return jsonify({"message": "Shift request deleted successfully"}), 200
