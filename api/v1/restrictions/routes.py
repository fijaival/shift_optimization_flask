from extensions import db  # これは書き替え

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from .models import Restriction
from .schemas import restriction_schema, restrictions_schema

restrictions_bp = Blueprint('restrictions', __name__)

# 制約登録


@restrictions_bp.route('/', methods=['POST'])
@jwt_required()
def add_restriction():
    data = request.json
    errors = restriction_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    new_restriction = Restriction(name=data['name'])

    db.session.add(new_restriction)
    db.session.commit()
    new_restriction_id = new_restriction.id
    db.session.close()

    return jsonify({"message": "Restriction added successfully!", "id": new_restriction_id}), 201

# 制約情報取得


@restrictions_bp.route('/', methods=["GET"])
@jwt_required()
def get_restriction():
    data = Restriction.query.all()
    return jsonify(restrictions_schema.dump(data))

# 制約情報削除


@restrictions_bp.route('/<int:res_id>', methods=['DELETE'])
@jwt_required()
def delete_restriction(res_id):
    restriction = db.session.query(Restriction).filter_by(id=res_id).first()

    if not restriction:
        return jsonify({"message": "Restriction not found"}), 404

    db.session.delete(restriction)
    db.session.commit()

    return jsonify({"message": "Restriction deleted successfully!"}), 200
