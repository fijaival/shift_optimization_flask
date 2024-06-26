from flask import Blueprint, jsonify, request
from api.error import InvalidAPIUsage
from extensions import Base, jwt_required, self_facility_required
from ..service.facilities import validate_and_create_facility_service, delete_facility_service, get_facility_service, add_qualification_to_facility_service, delete_qualification_from_facility_service, add_constraint_to_facility_service, delete_constraint_from_facility_service, add_task_to_facility_service, delete_task_from_facility_service

facilities_bp = Blueprint('facilities', __name__)


@facilities_bp.route('/', methods=['POST'])
# @jwt_required()
def add_facility():
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
        return InvalidAPIUsage("Facility not found", 404)
    return facility, 200


@facilities_bp.route('/<int:facility_id>/qualifications', methods=['POST'])
@self_facility_required
def add_qualification_to_facility(facility_id):
    """Add a qualification to a facility."""
    data = request.json
    res = add_qualification_to_facility_service(facility_id, data)
    if not res:
        raise InvalidAPIUsage("Qualification not found", 404)
    return res, 201


@facilities_bp.route('/<int:facility_id>/qualifications/<int:qualification_id>', methods=['DELETE'])
@self_facility_required
def delete_qualification_from_facility(facility_id, qualification_id):
    res = delete_qualification_from_facility_service(facility_id, qualification_id)
    if not res:
        raise InvalidAPIUsage("Qualification not found", 404)
    return res, 200


@facilities_bp.route('/<int:facility_id>/constraints', methods=['POST'])
@self_facility_required
def add_constraint_to_facility(facility_id):
    """Add a constraints to a facility."""
    data = request.json
    res = add_constraint_to_facility_service(facility_id, data)
    if not res:
        raise InvalidAPIUsage("Constraint not found", 404)
    return res, 201


@facilities_bp.route('/<int:facility_id>/constraints/<int:constraint_id>', methods=['DELETE'])
@self_facility_required
def delete_constraint_from_facility(facility_id, constraint_id):
    res = delete_constraint_from_facility_service(facility_id, constraint_id)
    if not res:
        raise InvalidAPIUsage("Constraint not found", 404)
    return res, 200


@facilities_bp.route('/<int:facility_id>/tasks', methods=['POST'])
@self_facility_required
def add_task_to_facility(facility_id):
    """Add a tasks to a facility."""
    data = request.json
    res = add_task_to_facility_service(facility_id, data)
    if not res:
        raise InvalidAPIUsage("Task not found", 404)
    return res, 201


@facilities_bp.route('/<int:facility_id>/tasks/<int:task_id>', methods=['DELETE'])
@self_facility_required
def delete_task_from_facility(facility_id, task_id):
    res = delete_task_from_facility_service(facility_id, task_id)
    if not res:
        raise InvalidAPIUsage("Task not found", 404)
    return res, 200
