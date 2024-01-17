from extensions import db

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..dependencies import EmployeeDependency
from ..restrictions import Restriction
from ..qualifications import Qualification
from ..employee_qualifications import EmployeeQualification
from ..employee_restrictions import EmployeeRestriction
from .models import Employee
from .schemas import employee_schema, employees_schema

employees_bp = Blueprint('employees', __name__)

# GET(全件参照)


@employees_bp.route('/', methods=["GET"])
@jwt_required()
def get_all_employees():
    employees = Employee.query.all()
    all_employees_data = []

    for employee in employees:
        # 従業員の基本情報
        employee_data = {
            "id": employee.id,
            "last_name": employee.last_name,
            "first_name": employee.first_name,
            "qualifications": [],
            "restrictions": [],
            "dependencies": []
        }

        # 資格情報の取得
        for eq in employee.qualifications:
            qualification = db.session.query(Qualification).filter_by(
                id=eq.qualification_id).first()
            if qualification:
                employee_data["qualifications"].append({
                    "id": qualification.id,
                    "name": qualification.name
                })

        # 制限情報の取得
        for er in employee.restrictions:
            restriction = db.session.query(Restriction).filter_by(
                id=er.restriction_id).first()
            if restriction:
                employee_data["restrictions"].append({
                    "id": restriction.id,
                    "name": restriction.name,
                    "value": er.value
                })

        # 依存関係の取得
        for dep in employee.dependencies:
            required_employee = db.session.query(Employee).filter_by(
                id=dep.required_employee_id).first()
            if required_employee:
                employee_data["dependencies"].append({
                    "id": required_employee.id,
                    "last_name": required_employee.last_name,
                    "first_name": required_employee.first_name
                })

        all_employees_data.append(employee_data)

    return jsonify(all_employees_data)


# GET(１件取得)


@employees_bp.route('/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee_details(employee_id):
    employee = db.session.query(Employee).filter_by(id=employee_id).first()

    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    # 従業員の基本情報
    employee_data = {
        "id": employee.id,
        "last_name": employee.last_name,
        "first_name": employee.first_name,
        "qualifications": [],
        "restrictions": [],
        "dependencies": []
    }

    # 資格情報の取得
    for eq in employee.qualifications:
        qualification = db.session.query(Qualification).filter_by(
            id=eq.qualification_id).first()
        if qualification:
            employee_data["qualifications"].append({
                "id": qualification.id,
                "name": qualification.name
            })

    # 制限情報の取得
    for er in employee.restrictions:
        restriction = db.session.query(Restriction).filter_by(
            id=er.restriction_id).first()
        if restriction:
            employee_data["restrictions"].append({
                "id": restriction.id,
                "name": restriction.name,
                "value": er.value
            })

    # 依存関係の取得
    for dep in employee.dependencies:
        required_employee = db.session.query(Employee).filter_by(
            id=dep.required_employee_id).first()
        if required_employee:
            employee_data["dependencies"].append({
                "id": required_employee.id,
                "last_name": required_employee.last_name,
                "first_name": required_employee.first_name
            })

    return jsonify(employee_data)

# 従業員情報の追加


@employees_bp.route('', methods=['POST'])
@jwt_required()
def add_employee():
    data = request.json
    new_employee = Employee(
        last_name=data['last_name'],
        first_name=data['first_name']
    )

    # 資格の情報を追加
    if 'qualifications' in data:
        for q_id in data['qualifications']:
            emp_qualification = EmployeeQualification(qualification_id=q_id)
            new_employee.qualifications.append(emp_qualification)

    # 制限の情報を追加
    if 'restrictions' in data:
        for r in data['restrictions']:
            emp_restriction = EmployeeRestriction(
                restriction_id=r['id'], value=r['value'])
            new_employee.restrictions.append(emp_restriction)

    # 依存関係の情報を追加
    if 'dependencies' in data:
        for d_id in data['dependencies']:
            dependency = EmployeeDependency(required_employee_id=d_id)
            new_employee.dependencies.append(dependency)

    db.session.add(new_employee)
    db.session.commit()

    return jsonify({"message": "Employee added successfully!", "id": new_employee.id}), 201

# 従業員の削除


@employees_bp.route('/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):

    employee = db.session.query(Employee).filter_by(id=employee_id).first()

    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    # 関連する資格情報の削除
    db.session.query(EmployeeQualification).filter_by(
        employee_id=employee_id).delete()

    # 関連する制限情報の削除
    db.session.query(EmployeeRestriction).filter_by(
        employee_id=employee_id).delete()

    # 関連する依存関係の削除
    db.session.query(EmployeeDependency).filter((EmployeeDependency.dependent_employee_id == employee_id) | (
        EmployeeDependency.required_employee_id == employee_id)).delete()

    # 従業員の削除
    db.session.delete(employee)
    db.session.commit()

    return jsonify({"message": "Employee deleted successfully!"}), 200

# 従業員の基本情報編集


@employees_bp.route('/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    employee = db.session.query(Employee).filter_by(id=employee_id).first()

    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    data = request.json
    errors = employee_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    employee.last_name = data['last_name']
    employee.first_name = data['first_name']

    db.session.commit()

    return jsonify({"message": "Employee updated successfully!"}), 200
