from flask import Blueprint, jsonify
# from .drivers_requests import drivers_requests_bp
# from .drivers_shifts import drivers_shifts_bp

# from .shift_generation import shift_generation_bp#これは消すな
from .routes import auth_bp, dependencies_bp,  employees_bp, qualifications_bp, constraints_bp, shifts_bp, shifts_requests_bp, facilities_bp

api_v1_bp = Blueprint('api_v1', __name__)
print("ええで")

# エラーハンドリング


# 各リソースのBlueprintを登録
api_v1_bp.register_blueprint(employees_bp, url_prefix='/employees')
api_v1_bp.register_blueprint(qualifications_bp, url_prefix='/qualifications')

api_v1_bp.register_blueprint(constraints_bp, url_prefix='/constraints')

api_v1_bp.register_blueprint(dependencies_bp, url_prefix='/dependencies')
# api_v1_bp.register_blueprint(drivers_bp, url_prefix='/drivers')
api_v1_bp.register_blueprint(facilities_bp, url_prefix='/facilities')
api_v1_bp.register_blueprint(shifts_requests_bp, url_prefix='/shifts_requests')
# api_v1_bp.register_blueprint(drivers_requests_bp, url_prefix='/drivers_requests')
api_v1_bp.register_blueprint(
    shifts_bp, url_prefix='/shifts')
# api_v1_bp.register_blueprint(
#     drivers_shifts_bp, url_prefix='/drivers_shifts')
# api_v1_bp.register_blueprint(
#     shift_generation_bp, url_prefix='/shift_generation')
api_v1_bp.register_blueprint(
    auth_bp, url_prefix='/auth')
