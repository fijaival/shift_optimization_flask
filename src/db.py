from src import app
from src import db
from flask import Flask, render_template, request, redirect, jsonify

from sqlalchemy.engine import Engine
from sqlalchemy import event

from .models import Employee, Qualification, EmployeeQualification, Restriction, EmployeeRestriction, EmployeeDependency, Driver
from .shema import employee_schema, employees_schema, qualifications_schema, restriction_schema

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()

@app.before_first_request
def init():
    db.create_all()

#GET(全件参照)
@app.route('/employees', methods=["GET"])
def get_all_employees():
    data = Employee.query.all()
    return jsonify(employees_schema.dump(data))

#GET(１件取得)
@app.route('/employees/<int:employee_id>', methods=['GET'])
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
        qualification = db.session.query(Qualification).filter_by(id=eq.qualification_id).first()
        if qualification:
            employee_data["qualifications"].append({
                "id": qualification.id,
                "name": qualification.name
            })

    # 制限情報の取得
    for er in employee.restrictions:
        restriction = db.session.query(Restriction).filter_by(id=er.restriction_id).first()
        if restriction:
            employee_data["restrictions"].append({
                "id": restriction.id,
                "name": restriction.name,
                "value": er.value
            })

    # 依存関係の取得
    for dep in employee.dependencies:
        required_employee = db.session.query(Employee).filter_by(id=dep.required_employee_id).first()
        if required_employee:
            employee_data["dependencies"].append({
                "id": required_employee.id,
                "last_name": required_employee.last_name,
                "first_name": required_employee.first_name
            })

    return jsonify(employee_data)

#従業員情報の追加
@app.route('/employees', methods=['POST'])
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
            emp_restriction = EmployeeRestriction(restriction_id=r['id'], value=r['value'])
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
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):

    employee = db.session.query(Employee).filter_by(id=employee_id).first()

    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    # 関連する資格情報の削除
    db.session.query(EmployeeQualification).filter_by(employee_id=employee_id).delete()

    # 関連する制限情報の削除
    db.session.query(EmployeeRestriction).filter_by(employee_id=employee_id).delete()

    # 関連する依存関係の削除
    db.session.query(EmployeeDependency).filter((EmployeeDependency.dependent_employee_id == employee_id) | (EmployeeDependency.required_employee_id == employee_id)).delete()

    # 従業員の削除
    db.session.delete(employee)
    db.session.commit()

    return jsonify({"message": "Employee deleted successfully!"}), 200

#従業員の基本情報編集
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = db.session.query(Employee).filter_by(id=employee_id).first()

    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    data = request.json

    # 従業員の基本情報の更新
    if 'last_name' in data:
        employee.last_name = data['last_name']
    if 'first_name' in data:
        employee.first_name = data['first_name']
        
    db.session.commit()

    return jsonify({"message": "Employee updated successfully!"}), 200

#資格登録
@app.route('/qualifications', methods=['POST'])
def add_qualification():
    data = request.json
    new_qualification = Qualification(name=data['name'])
    
    db.session.add(new_qualification)
    db.session.commit()
    new_qualification_id = new_qualification.id
    db.session.close()
    
    return jsonify({"message": "Qualification added successfully!", "id": new_qualification_id}), 201

#資格取得
@app.route('/qualifications', methods=["GET"])
def get_qualifications():
    data = Qualification.query.all()
    return jsonify(qualifications_schema.dump(data))

#資格情報の削除
@app.route('/qualifications/<int:qual_id>', methods=['DELETE'])
def delete_qualification(qual_id):
    qualification = db.session.query(Qualification).filter_by(id=qual_id).first()

    if not qualification:
        return jsonify({"message": "Qualification not found"}), 404

    db.session.delete(qualification)
    db.session.commit()

    return jsonify({"message": "Qualification deleted successfully!"}), 200

#制約登録
@app.route('/restrictions', methods=['POST'])
def add_restriction():
    data = request.json
    new_restriction = Restriction(name=data['name'])
    
    db.session.add(new_restriction)
    db.session.commit()
    new_restriction_id = new_restriction.id
    db.session.close()
    
    return jsonify({"message": "Restriction added successfully!", "id": new_restriction_id}), 201

#制約情報取得
@app.route('/restrictions', methods=["GET"])
def get_restriction():
    data = Restriction.query.all()
    return jsonify(restriction_schema.dump(data))

#制約情報削除
@app.route('/restrictions/<int:res_id>', methods=['DELETE'])
def delete_restriction(res_id):
    restriction = db.session.query(Restriction).filter_by(id=res_id).first()

    if not restriction:
        return jsonify({"message": "Restriction not found"}), 404

    db.session.delete(restriction)
    db.session.commit()

    return jsonify({"message": "Restriction deleted successfully!"}), 200

#全従業員の資格情報取得
@app.route('/employees_qualifications', methods=['GET'])
def get_all_employee_qualifications():
    
    # employee_qualificationsテーブルとemployeesテーブルを結合して、必要な情報を取得
    results = db.session.query(EmployeeQualification, Employee).join(Employee, Employee.id == EmployeeQualification.employee_id).all()

    qualifications_data = []
    for eq, emp in results:
        qualification = db.session.query(Qualification).filter_by(id=eq.qualification_id).first()
        qualifications_data.append({
            "employee_qualification_id": eq.id,
            "employee_id": emp.id,
            "employee_name": f"{emp.last_name} {emp.first_name}",
            "qualification_id": qualification.id,
            "qualification_name": qualification.name
        })

    return jsonify(qualifications_data)

#特定の従業員の資格情報追加（すでにある資格情報を追加できないようにフロント実装すべし）
@app.route('/employees_qualifications', methods=['POST'])
def add_employee_qualification():
    data = request.json

    # 必要なデータがPOSTリクエストに含まれているか確認
    if not all(key in data for key in ["employee_id", "qualification_id"]):
        return jsonify({"message": "Missing data"}), 400

    # 従業員が存在するか確認
    employee = db.session.query(Employee).filter_by(id=data['employee_id']).first()
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    # 資格が存在するか確認
    qualification = db.session.query(Qualification).filter_by(id=data['qualification_id']).first()
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
@app.route('/employees_qualifications/<int:eq_id>', methods=['DELETE'])
def delete_employee_qualification(eq_id):
    emp_qualification = db.session.query(EmployeeQualification).filter_by(id=eq_id).first()

    if not emp_qualification:
        return jsonify({"message": "Employee qualification not found"}), 404

    db.session.delete(emp_qualification)
    db.session.commit()

    return jsonify({"message": "Employee qualification deleted successfully!"}), 200

#全従業員の制限情報取得
@app.route('/employees_restrictions', methods=['GET'])
def get_all_employee_restrictions():
    
    # employees_restrictionsテーブルとemployeesテーブルを結合して、必要な情報を取得
    results = db.session.query(EmployeeRestriction, Employee).join(Employee, Employee.id == EmployeeRestriction.employee_id).all()

    restrictions_data = []
    for er, emp in results:
        restriction = db.session.query(Restriction).filter_by(id=er.restriction_id).first()
        restrictions_data.append({
            "employee_restriction_id": er.id,
            "employee_id": emp.id,
            "employee_name": f"{emp.last_name} {emp.first_name}",
            "restriction_id": restriction.id,
            "restriction_name": restriction.name,
            "value": er.value
        })

    return jsonify(restrictions_data)

#特定の従業員の制限情報追加 （すでにある制限情報を追加でいないようにフロント実装すべし）
@app.route('/employees_restrictions', methods=['POST'])
def add_employee_restriction():
    data = request.json

    # 必要なデータがPOSTリクエストに含まれているか確認
    if not all(key in data for key in ["employee_id", "restriction_id", "value"]):
        return jsonify({"message": "Missing data"}), 400

    # 従業員が存在するか確認
    employee = db.session.query(Employee).filter_by(id=data['employee_id']).first()
    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    # 制限が存在するか確認
    restriction = db.session.query(Restriction).filter_by(id=data['restriction_id']).first()
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

#特定の従業員の制限情報削除
@app.route('/employees_restrictions/<int:er_id>', methods=['DELETE'])
def delete_employee_restriction(er_id):
    emp_restriction = db.session.query(EmployeeRestriction).filter_by(id=er_id).first()

    if not emp_restriction:
        return jsonify({"message": "Employee restriction not found"}), 404

    db.session.delete(emp_restriction)
    db.session.commit()

    return jsonify({"message": "Employee restriction deleted successfully!"}), 200

#特定の従業員の制限情報更新
@app.route('/employees_restrictions/<int:er_id>', methods=['PUT'])
def update_employee_restriction(er_id):
    emp_restriction = db.session.query(EmployeeRestriction).filter_by(id=er_id).first()

    if not emp_restriction:
        return jsonify({"message": "Employee restriction not found"}), 404

    data = request.json

    # 制限情報の更新
    if 'value' in data:
        emp_restriction.value = data['value']

    db.session.commit()

    return jsonify({"message": "Employee restriction updated successfully!"}), 200

#全依存関係の取得
@app.route('/dependencies', methods=['GET'])
def get_all_dependencies():
    
    # dependenciesテーブルから情報を取得
    dependencies = db.session.query(EmployeeDependency).all()

    dependencies_data = []
    for dep in dependencies:
        dependent_employee = db.session.query(Employee).filter_by(id=dep.dependent_employee_id).first()
        required_employee = db.session.query(Employee).filter_by(id=dep.required_employee_id).first()

        if dependent_employee and required_employee:
            dependencies_data.append({
                "dependency_id": dep.id,
                "dependent_employee_id": dependent_employee.id,
                "dependent_employee_name": f"{dependent_employee.last_name} {dependent_employee.first_name}",
                "required_employee_id": required_employee.id,
                "required_employee_name": f"{required_employee.last_name} {required_employee.first_name}"
            })

    return jsonify(dependencies_data)

#依存関係の追加
@app.route('/dependencies', methods=['POST'])
def add_dependency():
    data = request.json

    # 必要なデータがPOSTリクエストに含まれているか確認
    if not all(key in data for key in ["dependent_employee_id", "required_employee_id"]):
        return jsonify({"message": "Missing data"}), 400

    # dependent_employeeが存在するか確認
    dependent_employee = db.session.query(Employee).filter_by(id=data['dependent_employee_id']).first()
    if not dependent_employee:
        return jsonify({"message": "Dependent employee not found"}), 404

    # required_employeeが存在するか確認
    required_employee = db.session.query(Employee).filter_by(id=data['required_employee_id']).first()
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

#特定の依存関係の更新
@app.route('/dependencies/<int:dep_id>', methods=['PUT'])
def update_dependency(dep_id):
    dependency = db.session.query(EmployeeDependency).filter_by(id=dep_id).first()

    if not dependency:
        return jsonify({"message": "Dependency not found"}), 404

    data = request.json

    # 依存関係の更新
    if 'dependent_employee_id' in data:
        dependent_employee = db.session.query(Employee).filter_by(id=data['dependent_employee_id']).first()
        if not dependent_employee:
            return jsonify({"message": "Dependent employee not found"}), 404
        dependency.dependent_employee_id = data['dependent_employee_id']

    if 'required_employee_id' in data:
        required_employee = db.session.query(Employee).filter_by(id=data['required_employee_id']).first()
        if not required_employee:
            return jsonify({"message": "Required employee not found"}), 404
        dependency.required_employee_id = data['required_employee_id']

    db.session.commit()

    return jsonify({"message": "Dependency updated successfully!"}), 200

#特定の依存関係の削除
@app.route('/dependencies/<int:dep_id>', methods=['DELETE'])
def delete_dependency(dep_id):
    dependency = db.session.query(EmployeeDependency).filter_by(id=dep_id).first()

    if not dependency:
        return jsonify({"message": "Dependency not found"}), 404

    db.session.delete(dependency)
    db.session.commit()

    return jsonify({"message": "Dependency deleted successfully!"}), 200

#全専属ドライバー取得
@app.route('/drivers', methods=["GET"])
def get_all_drivers():
    data = Driver.query.all()
    return jsonify(employees_schema.dump(data))

#ドライバー追加
@app.route('/drivers', methods=['POST'])
def add_driver():
    data = request.json
    new_driver = Driver(
        last_name=data['last_name'],
        first_name=data['first_name']
    )

    db.session.add(new_driver)
    db.session.commit()

    return jsonify({"message": "driver added successfully!", "id": new_driver.id}), 201


#ドライバー追加削除
@app.route('/drivers/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    driver = db.session.query(Driver).filter_by(id=driver_id).first()

    if not driver:
        return jsonify({"message": "driver not found"}), 404

    db.session.delete(driver)
    db.session.commit()

    return jsonify({"message": "driver deleted successfully!"}), 200
