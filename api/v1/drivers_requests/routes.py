from extensions import db

from flask import Blueprint, jsonify, request
from datetime import datetime
from sqlalchemy import extract

from ..drivers import Driver
from .models import DriversRequests

drivers_requests_bp = Blueprint('drivers_requests', __name__)


# 特定の月のシフト希望取得
@drivers_requests_bp.route('/<int:year>/<int:month>', methods=['GET'])
def get_shift_requests_for_month(year, month):
    # 指定された年と月のシフト希望を取得
    shift_requests = DriversRequests.query.filter(
        extract('year', DriversRequests.date) == year,
        extract('month', DriversRequests.date) == month
    ).all()

    # シフト希望データのシリアライズ（または適切な形式への変換）が必要
    shift_requests_data = [{'id': sr.id, 'driver_id': sr.driver_id, 'date': sr.date.strftime(
        '%Y-%m-%d'), 'type_of_vacation': sr.type_of_vacation} for sr in shift_requests]

    return jsonify(shift_requests_data)

# 希望シフト追加


@drivers_requests_bp.route('/', methods=['POST'])
def add_or_update_shift_request():
    data = request.json

    # データのバリデーション
    if 'driver_id' not in data or not isinstance(data['driver_id'], int):
        return jsonify({'message': 'Invalid or missing driver_id'}), 400

    if 'date' not in data:
        return jsonify({'message': 'Missing date'}), 400

    try:
        shift_date = datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    if 'type_of_vacation' not in data or data['type_of_vacation'] not in ['有', '公']:
        return jsonify({'message': 'Invalid or missing type_of_vacation'}), 400

    # 従業員が存在するかどうかを確認
    driver = Driver.query.get(data['driver_id'])
    if not driver:
        return jsonify({"message": "driver not found"}), 404

    # 既存のシフト希望の検索と更新、または新しいシフト希望の追加
    shift_request = DriversRequests.query.filter_by(
        driver_id=data['driver_id'], date=shift_date).first()

    if shift_request:
        shift_request.type_of_vacation = data['type_of_vacation']
    else:
        new_request = DriversRequests(
            driver_id=data['driver_id'],
            date=shift_date,
            type_of_vacation=data['type_of_vacation']
        )
        db.session.add(new_request)

    db.session.commit()
    return jsonify({"message": "Drivers shift request updated successfully"}), 200


# 希望シフト削除
@drivers_requests_bp.route('/<int:request_id>', methods=['DELETE'])
def delete_shift_request(request_id):
    shift_request = DriversRequests.query.get(request_id)

    if not shift_request:
        return jsonify({"message": "Drivers shift request not found"}), 404

    db.session.delete(shift_request)
    db.session.commit()
    return jsonify({"message": "Drivers shift request deleted successfully"}), 200
