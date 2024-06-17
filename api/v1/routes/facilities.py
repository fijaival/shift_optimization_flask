from flask import Blueprint, jsonify, request

from extensions import Base, jwt_required, self_facility_required

from ..validators import post_facility_schema, post_qualification_schema, post_constraint_schema
from ..models import Facility, FacilitySchema, Qualification, Constraint
from api.error import InvalidAPIUsage
from ..service.facilities import validate_and_create_facility_service, delete_facility_service, get_facility_service, add_qualification_to_facility_service, delete_qualification_from_facility_service, add_constraint_to_facility_service, delete_constraint_from_facility_service

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
    res = validate_and_create_facility_service(data)
    return res, 201


@facilities_bp.route('/<int:facility_id>', methods=['DELETE'])
@jwt_required()
def delete_facility(facility_id):
    """Delete a facility from the database.userより上の権限必要?"""
    facility = delete_facility_service(facility_id)
    if not facility:
        raise InvalidAPIUsage("Facility not found", 404)
    return jsonify({"message": "Facility deleted successfully!"}), 200


@facilities_bp.route('/<int:facility_id>', methods=['GET'])
@self_facility_required
def get_facility(facility_id):
    """Get a facility by its ID."""
    facility = get_facility_service(facility_id)
    if not facility:
        return jsonify({"message": "Facility not found"}), 404
    return facility, 200


@facilities_bp.route('/<int:facility_id>/qualifications', methods=['POST'])
@self_facility_required
def add_qualification_to_facility(facility_id):
    """Add a qualification to a facility."""
    data = request.json
    res = add_qualification_to_facility_service(facility_id, data)
    return res, 201


@facilities_bp.route('/<int:facility_id>/qualifications/<int:qualification_id>', methods=['DELETE'])
@self_facility_required
def delete_qualification_from_facility(facility_id, qualification_id):
    try:
        if delete_qualification_from_facility_service(facility_id, qualification_id):
            return jsonify({"message": "Qualification deleted successfully!"}), 200
    except InvalidAPIUsage as e:
        return jsonify({"message": e.message}), e.status_code


@facilities_bp.route('/<int:facility_id>/constraints', methods=['POST'])
@self_facility_required
def add_constraint_to_facility(facility_id):
    data = request.json
    res = add_constraint_to_facility_service(facility_id, data)
    return res, 201


@facilities_bp.route('/<int:facility_id>/constraints/<int:constraint_id>', methods=['DELETE'])
@self_facility_required
def delete_constraint_from_facility(facility_id, constraint_id):
    try:
        if delete_constraint_from_facility_service(facility_id, constraint_id):
            return jsonify({"message": "Constraint deleted successfully!"}), 200
    except InvalidAPIUsage as e:
        return jsonify({"message": e.message}), e.status_code
