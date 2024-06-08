from flask import Blueprint, jsonify, request

from extensions import db, jwt_required, self_facility_required
# from extensions.auth import jwt_required, self_facility_required

from ..validators import post_facility_schema, post_qualification_schema, post_constraint_schema
from ..models import Facility, FacilitySchema, Qualification, Constraint
from api.error import InvalidAPIUsage

facilities_bp = Blueprint('facilities', __name__)


@facilities_bp.route('/', methods=['GET'])
@jwt_required()
def get_facilities():
    return jsonify({"message": "Facilities data will be returned here."})


@facilities_bp.route('/', methods=['POST'])
@jwt_required()
def add_facility():
    data = request.json
    error = post_facility_schema.validate(data)
    if error:
        raise InvalidAPIUsage(error)
    new_facility = Facility(**data)
    db.session.add(new_facility)
    db.session.commit()

    res = FacilitySchema().dump(new_facility)
    return res, 201


@facilities_bp.route('/<int:facility_id>', methods=['GET'])
@self_facility_required
def get_facility(facility_id):
    facility = db.session.query(Facility).filter_by(
        facility_id=facility_id).first()

    if not facility:
        return jsonify({"message": "Facility not found"}), 404

    res = FacilitySchema().dump(facility)
    return res, 200


@facilities_bp.route('/<int:facility_id>/qualifications', methods=['POST'])
@self_facility_required
def add_qualification_to_facility(facility_id):
    data = request.json
    error = post_qualification_schema.validate(data)
    if error:
        raise InvalidAPIUsage(error)

    qualification = Qualification.query.filter_by(name=data['name']).first()
    if not qualification:
        qualification = Qualification(**data)
        db.session.add(qualification)
        db.session.commit()

    facility = Facility.query.filter_by(facility_id=facility_id).first()
    if not facility:
        raise InvalidAPIUsage("Facility not found", 404)

    if any(q.name == data['name'] for q in facility.qualifications):
        raise InvalidAPIUsage(
            "The facility already has its qualification", 400)

    facility.qualifications.append(qualification)
    db.session.commit()
    res = FacilitySchema().dump(facility)
    return res, 201


@facilities_bp.route('/<int:facility_id>/constraints', methods=['POST'])
@self_facility_required
def add_constraint_to_facility(facility_id):
    data = request.json
    error = post_constraint_schema.validate(data)
    if error:
        raise InvalidAPIUsage(error)

    constraint = Constraint.query.filter_by(name=data['name']).first()
    if not constraint:
        constraint = Constraint(**data)
        db.session.add(constraint)
        db.session.commit()

    facility = Facility.query.filter_by(facility_id=facility_id).first()
    if not facility:
        raise InvalidAPIUsage("Facility not found", 404)

    if any(q.name == data['name'] for q in facility.constraints):
        raise InvalidAPIUsage(
            "The facility already has its constraint", 400)

    facility.constraints.append(constraint)
    db.session.commit()
    res = FacilitySchema().dump(facility)
    return res, 201
