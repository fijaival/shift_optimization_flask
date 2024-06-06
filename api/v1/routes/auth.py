from extensions import db


from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity,
                                get_jwt, set_access_cookies, set_refresh_cookies, unset_jwt_cookies,
                                )
from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from ..models import User, UserSchema, TokenBlocklist
# from ..schemas import user_schema, users_schema
from ..validators import post_user_schema, login_user_schema
from api.error import InvalidAPIUsage


auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/signup', methods=['POST'])
def signin():
    input_data = request.json
    errors = post_user_schema.validate(input_data)
    if errors:
        raise InvalidAPIUsage(errors)

    user = User.query.filter_by(username=input_data["username"]).first()
    if user:
        raise InvalidAPIUsage("User already exists")
    new_user = User(**input_data)
    db.session.add(new_user)
    db.session.commit()

    res = UserSchema().dump(new_user)
    return res, 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    errors = login_user_schema.validate(data)
    if errors:
        raise InvalidAPIUsage(errors)
    auth_user = User.query.filter_by(username=data['username']).first()

    if auth_user is not None and auth_user.check_password(data['password']):
        access_token = create_access_token(identity=auth_user.user_id)
        refresh_token = create_refresh_token(identity=auth_user.user_id)
        resp = jsonify({'login': True})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, 200
    else:
        raise InvalidAPIUsage('Invalid User.', 401)


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    resp = jsonify({'refresh': True})
    resp.set_cookie('access_token_cookie', '', expires=datetime(1970, 1, 1))
    resp.set_cookie('access_token_cookie', access_token,
                    samesite='None', secure=True)
    return resp, 200


@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def modify_token():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    now = datetime.now(timezone.utc)
    new_block_token = TokenBlocklist(jti=jti, type=ttype, created_at=now)
    db.session.add(new_block_token)
    db.session.commit()
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200
