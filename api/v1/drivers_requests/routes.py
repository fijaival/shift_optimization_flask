from extensions import db

from flask import Blueprint, jsonify, request
from datetime import datetime
from sqlalchemy import extract

from ..drivers import Driver
from .models import DriversRequests
from .schemas import drivers_request_schema

drivers_requests_bp = Blueprint('drivers_requests', __name__)


# 特定の月のシフト希望取得
@drivers_requests_bp.route('/<int:year>/<int:month>', methods=['GET'])
def get_shift_requests_for_month(year, month):
    shift_requests = DriversRequests.query.filter(
        extract('year', DriversRequests.date) == year,
        extract('month', DriversRequests.date) == month
    ).all()
    shift_requests_data = drivers_request_schema.dump(
        shift_requests, many=True)
    return jsonify(shift_requests_data)

# 希望シフト追加


@drivers_requests_bp.route('/', methods=['POST'])
def add_or_update_shift_request():
    requests_data = request.json

    errors = drivers_request_schema.validate(requests_data, many=True)
    if errors:
        return jsonify(errors), 400
    for data in requests_data:
        driver_id = data['driver_id']
        shift_date = datetime.strptime(data['date'], '%Y-%m-%d')
        type_of_vacation = data['type_of_vacation']
        # 従業員が存在するかどうかを確認
        driver = Driver.query.get(driver_id)
        if not driver:
            continue  # スキップ

        # 既存のシフト希望の検索と更新、または新しいシフト希望の追加
        shift_request = DriversRequests.query.filter_by(
            driver_id=driver_id, date=shift_date).first()

        if shift_request:
            shift_request.type_of_vacation = type_of_vacation
        else:
            new_request = DriversRequests(
                driver_id=driver_id,
                date=shift_date,
                type_of_vacation=type_of_vacation
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
