from extensions import db

from flask import Blueprint, jsonify, request
from ..employees import employees_schema
from .models import Driver
from .schemas import driver_schema, drivers_schema


drivers_bp = Blueprint('drivers', __name__)

# 全専属ドライバー取得


@drivers_bp.route('/', methods=["GET"])
def get_all_drivers():
    data = Driver.query.all()
    return jsonify(drivers_schema.dump(data, many=True))
# ドライバー追加


@drivers_bp.route('/', methods=['POST'])
def add_driver():
    data = request.json
    errors = driver_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    new_driver = Driver(
        last_name=data['last_name'],
        first_name=data['first_name']
    )

    db.session.add(new_driver)
    db.session.commit()

    return jsonify({"message": "driver added successfully!", "id": new_driver.id}), 201


# ドライバー削除
@drivers_bp.route('/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    driver = db.session.query(Driver).filter_by(id=driver_id).first()

    if not driver:
        return jsonify({"message": "driver not found"}), 404

    db.session.delete(driver)
    db.session.commit()

    return jsonify({"message": "driver deleted successfully!"}), 200
