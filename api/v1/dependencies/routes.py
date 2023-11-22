from extensions import db

from flask import Blueprint, jsonify, request

from .models import EmployeeDependency
from .schemas import employee_dependency_schema


dependencies_bp = Blueprint('dependencies', __name__)

# 循環参照を防ぐための全ての関数内でのEmployeesのローカルインポートは直したい。
# 全依存関係の取得


@dependencies_bp.route('/', methods=['GET'])
def get_all_dependencies():
    from ..employees import Employee

    # dependenciesテーブルから情報を取得
    dependencies = db.session.query(EmployeeDependency).all()
    dependencies_data = []
    for dep in dependencies:
        dependent_employee = db.session.query(Employee).filter_by(
            id=dep.dependent_employee_id).first()
        required_employee = db.session.query(Employee).filter_by(
            id=dep.required_employee_id).first()

        if dependent_employee and required_employee:
            dependencies_data.append({
                "dependency_id": dep.id,
                "dependent_employee_id": dependent_employee.id,
                "dependent_employee_name": f"{dependent_employee.last_name} {dependent_employee.first_name}",
                "required_employee_id": required_employee.id,
                "required_employee_name": f"{required_employee.last_name} {required_employee.first_name}"
            })

    return jsonify(dependencies_data)

# 依存関係の追加


@dependencies_bp.route('/', methods=['POST'])
def add_dependency():
    from ..employees import Employee
    data = request.json

    errors = employee_dependency_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # dependent_employeeが存在するか確認
    dependent_employee = db.session.query(Employee).filter_by(
        id=data['dependent_employee_id']).first()
    if not dependent_employee:
        return jsonify({"message": "Dependent employee not found"}), 404

    # required_employeeが存在するか確認
    required_employee = db.session.query(Employee).filter_by(
        id=data['required_employee_id']).first()
    if not required_employee:
        return jsonify({"message": "Required employee not found"}), 404

    # 新たな依存関係を追加
    new_dependency = EmployeeDependency(
        dependent_employee_id=data['dependent_employee_id'],
        required_employee_id=data['required_employee_id']
    )
    db.session.add(new_dependency)
    db.session.commit()

    return jsonify({"message": "Dependency added successfully!", "id": new_dependency.id}), 201

# 特定の依存関係の更新


@dependencies_bp.route('/<int:dep_id>', methods=['PUT'])
def update_dependency(dep_id):
    from ..employees import Employee

    data = request.json
    errors = employee_dependency_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    dependency = db.session.query(
        EmployeeDependency).filter_by(id=dep_id).first()

    if not dependency:
        return jsonify({"message": "Dependency not found"}), 404

    # 依存関係の更新
    if 'dependent_employee_id' in data:
        dependent_employee = db.session.query(Employee).filter_by(
            id=data['dependent_employee_id']).first()
        if not dependent_employee:
            return jsonify({"message": "Dependent employee not found"}), 404
        dependency.dependent_employee_id = data['dependent_employee_id']

    if 'required_employee_id' in data:
        required_employee = db.session.query(Employee).filter_by(
            id=data['required_employee_id']).first()
        if not required_employee:
            return jsonify({"message": "Required employee not found"}), 404
        dependency.required_employee_id = data['required_employee_id']

    db.session.commit()

    return jsonify({"message": "Dependency updated successfully!"}), 200

# 特定の依存関係の削除


@dependencies_bp.route('/<int:dep_id>', methods=['DELETE'])
def delete_dependency(dep_id):
    from ..employees import Employee
    dependency = db.session.query(
        EmployeeDependency).filter_by(id=dep_id).first()

    if not dependency:
        return jsonify({"message": "Dependency not found"}), 404

    db.session.delete(dependency)
    db.session.commit()

    return jsonify({"message": "Dependency deleted successfully!"}), 200
