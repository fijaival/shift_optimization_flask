from extensions import db  # これは書き替え
from flask import Blueprint, jsonify, request
from .models import Qualification
from .schemas import qualification_schema, qualifications_schema

qualifications_bp = Blueprint('qualifications', __name__)


# 資格登録
@qualifications_bp.route('/', methods=['POST'])
def add_qualification():
    data = request.json
    errors = qualification_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    new_qualification = Qualification(name=data['name'])

    db.session.add(new_qualification)
    db.session.commit()
    new_qualification_id = new_qualification.id
    db.session.close()

    return jsonify({"message": "Qualification added successfully!", "id": new_qualification_id}), 201

# 資格取得


@qualifications_bp.route('/', methods=["GET"])
def get_qualifications():
    data = Qualification.query.all()
    return jsonify(qualifications_schema.dump(data))

# 資格情報の削除


@qualifications_bp.route('/<int:qual_id>', methods=['DELETE'])
def delete_qualification(qual_id):
    qualification = db.session.query(
        Qualification).filter_by(id=qual_id).first()

    if not qualification:
        return jsonify({"message": "Qualification not found"}), 404

    db.session.delete(qualification)
    db.session.commit()

    return jsonify({"message": "Qualification deleted successfully!"}), 200
