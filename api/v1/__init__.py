from flask import Blueprint, jsonify
from .routes import auth_bp,  employees_bp, shifts_bp,  facilities_bp, shifts_requests_bp
# from .shift_generation import shift_generation_bp#これは消すな
api_v1_bp = Blueprint('api_v1', __name__)


# 各リソースのBlueprintを登録
api_v1_bp.register_blueprint(employees_bp)
api_v1_bp.register_blueprint(facilities_bp, url_prefix='/facilities')
api_v1_bp.register_blueprint(
    shifts_bp, url_prefix='/shifts')

api_v1_bp.register_blueprint(
    auth_bp, url_prefix='/auth')
api_v1_bp.register_blueprint(shifts_requests_bp, url_prefix='/shifts_requests')
