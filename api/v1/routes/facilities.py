from flask import Blueprint, jsonify, request

from extensions import db, jwt_required, self_facility_required

from ..validators import post_facility_schema, post_qualification_schema, post_constraint_schema
from ..models import Facility, FacilitySchema, Qualification, Constraint
from api.error import InvalidAPIUsage

facilities_bp = Blueprint('facilities', __name__)


@facilities_bp.route('/', methods=['GET'])
@jwt_required()
def get_facilities():
    """Get all facilities.これが必要になるときはないかもしれない。"""
    return jsonify({"message": "Facilities data will be returned here."})


@facilities_bp.route('/', methods=['POST'])
# @jwt_required()
def add_facility():
    """Add a facility to the database.userより上の権限必要"""
    data = request.json
    error = post_facility_schema.validate(data)
    if error:
        raise InvalidAPIUsage(error)
    new_facility = Facility(**data)
    db.session.add(new_facility)
    db.session.commit()

    res = FacilitySchema().dump(new_facility)
    return res, 201


@facilities_bp.route('/<int:facility_id>', methods=['DELETE'])
@jwt_required()
def delete_facility(facility_id):
    """Delete a facility from the database.userより上の権限必要?"""
    try:
        facility = db.session.query(Facility).filter_by(
            facility_id=facility_id).first()

        if not facility:
            return jsonify({"message": "Facility not found"}), 404

        db.session.delete(facility)
        db.session.commit()
        return jsonify({"message": "Facility deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error occurred{e}"}), 500


@facilities_bp.route('/<int:facility_id>', methods=['GET'])
@self_facility_required
def get_facility(facility_id):
    """Get a facility by its ID."""
    facility = db.session.query(Facility).filter_by(
        facility_id=facility_id).first()

    if not facility:
        return jsonify({"message": "Facility not found"}), 404

    res = FacilitySchema().dump(facility)
    return res, 200


@facilities_bp.route('/<int:facility_id>/qualifications', methods=['POST'])
@self_facility_required
def add_qualification_to_facility(facility_id):
    """Add a qualification to a facility."""
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


@facilities_bp.route('/<int:facility_id>/qualifications/<int:qualification_id>', methods=['DELETE'])
@self_facility_required
def delete_qualification_from_facility(facility_id, qualification_id):
    facility = Facility.query.filter_by(facility_id=facility_id).first()
    if not facility:
        raise InvalidAPIUsage("Facility not found", 404)

    qualification = Qualification.query.filter_by(qualification_id=qualification_id).first()
    if not qualification:
        raise InvalidAPIUsage("Qualification not found", 404)

    if any(q.qualification_id == qualification_id for q in facility.qualifications):
        facility.qualifications.remove(qualification)
        db.session.commit()
        return jsonify({"message": "Qualification deleted successfully!"}), 200

    raise InvalidAPIUsage("The facility does not have this qualification", 400)


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


@facilities_bp.route('/<int:facility_id>/constraints/<int:constraint_id>', methods=['DELETE'])
@self_facility_required
def delete_constraint_from_facility(facility_id, constraint_id):
    facility = Facility.query.filter_by(facility_id=facility_id).first()
    if not facility:
        raise InvalidAPIUsage("Facility not found", 404)

    constraint = Constraint.query.filter_by(constraint_id=constraint_id).first()
    if not constraint:
        raise InvalidAPIUsage("Constraint not found", 404)

    if any(q.constraint_id == constraint_id for q in facility.constraints):
        facility.constraints.remove(constraint)
        db.session.commit()
        return jsonify({"message": "Constraint deleted successfully!"}), 200

    raise InvalidAPIUsage("The facility does not have this constraint", 400)
