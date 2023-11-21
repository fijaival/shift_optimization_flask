from extensions import db
from flask import Blueprint, jsonify, request
from sqlalchemy import extract
from datetime import datetime
from .models import DriversShift
from .schemas import drivers_shift_schema, drivers_shifts_schema
# Driverモデルのインポートが必要です
from ..drivers import Driver

drivers_shifts_bp = Blueprint('drivers_shifts', __name__)

# 専属ドライバーの特定の月のシフトを取得


@drivers_shifts_bp.route('/<int:year>/<int:month>', methods=["GET"])
def get_driver_shifts_for_month(year, month):
    shifts = DriversShift.query.filter(
        extract('year', DriversShift.date) == year,
        extract('month', DriversShift.date) == month
    ).all()
    return jsonify(drivers_shifts_schema.dump(shifts))

# 専属ドライバーのシフト登録


@drivers_shifts_bp.route('/', methods=['POST'])
def add_driver_shifts():
    shifts_data = request.json

    for shift_data in shifts_data:
        errors = drivers_shift_schema.validate(shift_data)
        if errors:
            return jsonify({"errors": errors}), 400
        # 従業員IDの存在を確認
        driver = Driver.query.get(shift_data['driver_id'])
        if not driver:
            return jsonify({"message": f"driver with ID {shift_data['driver_id']} not found"}), 404

        new_shift = DriversShift(
            driver_id=shift_data['driver_id'],
            date=datetime.strptime(shift_data['date'], '%Y-%m-%d').date(),
            type_of_work=shift_data['type_of_work']
        )
        db.session.add(new_shift)

    db.session.commit()
    return jsonify({
        "message": "Driver shifts added successfully!",
    }), 201

# 専属ドライバーのシフトの月単位での一括削除


@drivers_shifts_bp.route('/<int:year>/<int:month>', methods=['DELETE'])
def delete_driver_shift(year, month):
    shifts = DriversShift.query.filter(
        extract('year', DriversShift.date) == year,
        extract('month', DriversShift.date) == month
    ).all()

    # 見つかったシフトをすべて削除
    for shift in shifts:
        db.session.delete(shift)

    db.session.commit()
    return jsonify({"message": f"Driver shifts for {year}-{month} deleted successfully!"}), 200


# 専属ドライバーのシフトの更新
@drivers_shifts_bp.route('/', methods=['PUT'])
def update_driver_shifts():
    shifts_data = request.json
    not_found_shifts = []

    for shift_data in shifts_data:
        shift = DriversShift.query.get(shift_data['id'])
        if not shift:
            not_found_shifts.append(shift_data['id'])
            continue  # シフトが見つからなければこのシフトをスキップ

        # type_of_workのみを更新
        if 'type_of_work' in shift_data:
            shift.type_of_work = shift_data['type_of_work']

    db.session.commit()
    return jsonify({
        "message": "Driver shifts updated successfully!",
        "not_found_shifts": not_found_shifts
    }), 200 if not not_found_shifts else 207
