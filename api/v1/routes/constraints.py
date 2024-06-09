from extensions import db  # これは書き替え

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..models import Constraint
from ..schemas import constraint_schema, constraints_schema

constraints_bp = Blueprint('constraints', __name__)

# 制約登録


@constraints_bp.route('/', methods=['POST'])
@jwt_required()
def add_constraint():
    data = request.json
    errors = constraint_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    new_constraint = Constraint(name=data['name'])

    db.session.add(new_constraint)
    db.session.commit()
    new_constraint_id = new_constraint.id
    db.session.close()

    return jsonify({"message": "Constraint added successfully!", "id": new_constraint_id}), 201

# 制約情報取得


@constraints_bp.route('/', methods=["GET"])
@jwt_required()
def get_constraint():
    data = Constraint.query.all()
    return jsonify(constraints_schema.dump(data))

# 制約情報削除


@constraints_bp.route('/<int:res_id>', methods=['DELETE'])
@jwt_required()
def delete_constraint(res_id):
    constraint = db.session.query(Constraint).filter_by(id=res_id).first()

    if not constraint:
        return jsonify({"message": "Constraint not found"}), 404

    db.session.delete(constraint)
    db.session.commit()

    return jsonify({"message": "Constraint deleted successfully!"}), 200
