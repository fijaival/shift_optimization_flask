from flask import Blueprint
from .employees import employees_bp
from .qualifications import qualifications_bp
from .employee_qualifications import employees_qualifications_bp
from .restrictions import restrictions_bp
from .employee_restrictions import employees_restrictions_bp
from .dependencies import dependencies_bp
from .drivers import drivers_bp
from .shifts_requests import shifts_requests_bp
from .drivers_requests import drivers_requests_bp
from .shifts import shifts_bp

api_v1_bp = Blueprint('api_v1', __name__)

# 各リソースのBlueprintを登録
api_v1_bp.register_blueprint(employees_bp, url_prefix='/employees')
api_v1_bp.register_blueprint(qualifications_bp, url_prefix='/qualifications')
api_v1_bp.register_blueprint(
    employees_qualifications_bp, url_prefix='/employees_qualifications')
api_v1_bp.register_blueprint(restrictions_bp, url_prefix='/restrictions')
api_v1_bp.register_blueprint(
    employees_restrictions_bp, url_prefix='/employees_restrictions')
api_v1_bp.register_blueprint(dependencies_bp, url_prefix='/dependencies')
api_v1_bp.register_blueprint(drivers_bp, url_prefix='/drivers')

api_v1_bp.register_blueprint(shifts_requests_bp, url_prefix='/shifts_requests')
api_v1_bp.register_blueprint(
    drivers_requests_bp, url_prefix='/drivers_requests')
api_v1_bp.register_blueprint(
    shifts_bp, url_prefix='/shifts')
