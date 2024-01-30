from extensions import db

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..employees import Employee
from ..qualifications import Qualification

from .models import EmployeeQualification
from .schemas import employee_qualification_schema


employees_qualifications_bp = Blueprint('employees_qualifications', __name__)

# 全従業員の資格情報取得


@employees_qualifications_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_employee_qualifications():

    # employee_qualificationsテーブルとemployeesテーブルを結合して、必要な情報を取得
    results = db.session.query(EmployeeQualification, Employee).join(
        Employee, Employee.id == EmployeeQualification.employee_id).all()

    qualifications_data = []
    for eq, emp in results:
        qualification = db.session.query(Qualification).filter_by(
            id=eq.qualification_id).first()
        qualifications_data.append({
            "employee_qualification_id": eq.id,
            "employee_id": emp.id,
            "employee_name": f"{emp.last_name} {emp.first_name}",
            "qualification_id": qualification.id,
            "qualification_name": qualification.name
        })

    return jsonify(qualifications_data)

# 特定の従業員の資格情報追加（すでにある資格情報を追加できないようにフロント実装すべし）


@employees_qualifications_bp.route('', methods=['POST'])
@jwt_required()
def add_employee_qualification():
    data = request.json

    errors = employee_qualification_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # 従業員が存在するか確認
    employee = db.session.query(Employee).filter_by(
        id=data['employee_id']).first()
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    # 資格が存在するか確認
    qualification = db.session.query(Qualification).filter_by(
        id=data['qualification_id']).first()
    if not qualification:
        return jsonify({"message": "Qualification not found"}), 404

    # 資格情報を追加
    emp_qualification = EmployeeQualification(
        employee_id=data['employee_id'],
        qualification_id=data['qualification_id']
    )
    db.session.add(emp_qualification)
    db.session.commit()

    return jsonify({"message": "Employee qualification added successfully!", "id": emp_qualification.id}), 201

# 従業員の資格情報削除


@employees_qualifications_bp.route('/<int:eq_id>', methods=['DELETE'])
@jwt_required()
def delete_employee_qualification(eq_id):
    emp_qualification = db.session.query(
        EmployeeQualification).filter_by(id=eq_id).first()

    if not emp_qualification:
        return jsonify({"message": "Employee qualification not found"}), 404

    db.session.delete(emp_qualification)
    db.session.commit()

    return jsonify({"message": "Employee qualification deleted successfully!"}), 200
