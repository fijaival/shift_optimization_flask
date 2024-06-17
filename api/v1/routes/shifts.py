from sqlalchemy import extract, between
from extensions import Base


from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..models.shifts import Shift
from ..models.employees import Employee

# from ..schemas import shift_schema, shifts_schema
from datetime import datetime
from sqlalchemy import extract


shifts_bp = Blueprint('shifts', __name__)

# GETリクエスト（特定の年月のシフトを取得）


@shifts_bp.route('/<int:year>/<int:month>', methods=["GET"])
@jwt_required()
def get_shifts_for_month(year, month):

    shifts = Shift.query.filter(
        extract('year', Shift.date) == year,
        extract('month', Shift.date) == month,
    ).all()
    return jsonify(shifts_schema.dump(shifts))


# POSTリクエスト（シフトの登録）
@shifts_bp.route('/', methods=['POST'])
@jwt_required()
def add_shifts():
    shifts_data = request.json

    for shift_data in shifts_data:
        errors = shift_schema.validate(shift_data)
        if errors:
            return jsonify({"errors": errors}), 400
        # 従業員IDの存在を確認
        employee = Employee.query.get(shift_data['employee_id'])
        if not employee:
            return jsonify({"message": f"Employee with ID {shift_data['employee_id']} not found"}), 404

        shift_date = datetime.strptime(shift_data['date'], '%Y-%m-%d').date()
        new_shift = Shift(
            employee_id=shift_data['employee_id'],
            date=shift_date,
            type_of_work=shift_data['type_of_work']
        )
        db.session.add(new_shift)

    db.session.commit()
    return jsonify({"message": "Shifts added successfully!"}), 201

# シフトの月単位での一括削除


@shifts_bp.route('/<int:year>/<int:month>', methods=['DELETE'])
@jwt_required()
def delete_shift(year, month):
    shifts = Shift.query.filter(
        extract('year', Shift.date) == year,
        extract('month', Shift.date) == month
    ).all()

    # 見つかったシフトをすべて削除
    for shift in shifts:
        db.session.delete(shift)

    db.session.commit()
    return jsonify({"message": f"shifts for {year}-{month} deleted successfully!"}), 200


# PUTリクエスト（シフト情報の更新）
@shifts_bp.route('/', methods=['PUT'])
@jwt_required()
def update_shifts():
    shifts_data = request.json

    for shift_data in shifts_data:
        shift_id = shift_data['id']
        shift = Shift.query.get(shift_id)
        if not shift:
            continue  # シフトが見つからなければスキップ

        # 作業タイプの更新
        if 'type_of_work' in shift_data:
            shift.type_of_work = shift_data['type_of_work']

    db.session.commit()
    return jsonify({"message": "Shifts updated successfully!"}), 200
