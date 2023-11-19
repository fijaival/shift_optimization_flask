from extensions import db

from flask import Blueprint, jsonify, request
from ..restrictions import Restriction
from ..employees import Employee

from .models import EmployeeRestriction
from .schemas import employee_restriction_schema

employees_restrictions_bp = Blueprint('employees_restrictions', __name__)

# 全従業員の制限情報取得


@employees_restrictions_bp.route('/', methods=['GET'])
def get_all_employee_restrictions():

    # employees_restrictionsテーブルとemployeesテーブルを結合して、必要な情報を取得
    results = db.session.query(EmployeeRestriction, Employee).join(
        Employee, Employee.id == EmployeeRestriction.employee_id).all()

    restrictions_data = []
    for er, emp in results:
        restriction = db.session.query(Restriction).filter_by(
            id=er.restriction_id).first()
        restrictions_data.append({
            "employee_restriction_id": er.id,
            "employee_id": emp.id,
            "employee_name": f"{emp.last_name} {emp.first_name}",
            "restriction_id": restriction.id,
            "restriction_name": restriction.name,
            "value": er.value
        })

    return jsonify(restrictions_data)

# 特定の従業員の制限情報追加 （すでにある制限情報を追加でいないようにフロント実装すべし）


@employees_restrictions_bp.route('/', methods=['POST'])
def add_employee_restriction():
    data = request.json

    errors = employee_restriction_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # 従業員が存在するか確認
    employee = db.session.query(Employee).filter_by(
        id=data['employee_id']).first()
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    # 制限が存在するか確認
    restriction = db.session.query(Restriction).filter_by(
        id=data['restriction_id']).first()
    if not restriction:
        return jsonify({"message": "Restriction not found"}), 404

    # 制限情報を追加
    emp_restriction = EmployeeRestriction(
        employee_id=data['employee_id'],
        restriction_id=data['restriction_id'],
        value=data['value']
    )
    db.session.add(emp_restriction)
    db.session.commit()

    return jsonify({"message": "Employee restriction added successfully!", "id": emp_restriction.id}), 201

# 特定の従業員の制限情報削除


@employees_restrictions_bp.route('/<int:er_id>', methods=['DELETE'])
def delete_employee_restriction(er_id):
    emp_restriction = db.session.query(
        EmployeeRestriction).filter_by(id=er_id).first()

    if not emp_restriction:
        return jsonify({"message": "Employee restriction not found"}), 404

    db.session.delete(emp_restriction)
    db.session.commit()

    return jsonify({"message": "Employee restriction deleted successfully!"}), 200

# 特定の従業員の制限情報更新


@employees_restrictions_bp.route('/<int:er_id>', methods=['PUT'])
def update_employee_restriction(er_id):
    emp_restriction = db.session.query(
        EmployeeRestriction).filter_by(id=er_id).first()

    if not emp_restriction:
        return jsonify({"message": "Employee restriction not found"}), 404

    data = request.json
    errors = employee_restriction_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # 制限情報の更新
    if 'value' in data:
        emp_restriction.value = data['value']

    db.session.commit()

    return jsonify({"message": "Employee restriction updated successfully!"}), 200
