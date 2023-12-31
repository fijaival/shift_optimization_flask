from extensions import db
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity,
                                get_jwt, set_access_cookies, set_refresh_cookies, unset_jwt_cookies,
                                get_csrf_token)
from flask import Blueprint, jsonify, request, make_response
from datetime import datetime, timezone
from .models import User, TokenBlocklist
from .schemas import user_schema, users_schema
from extensions import jwt


auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/users', methods=["GET"])
def get_all_users():
    data = User.query.all()
    # この処理はテストのため処理が中途半端
    return jsonify(users_schema.dump(data, many=True))


@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.json
    errors = user_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    username = data['username']
    password = data['password']
    if password is None or username is None or password == "" or username == "":
        return jsonify({"msg": "password or username has not been entered"}), 400
    if len(password) < 4:
        return jsonify({"msg": "password is too short"}), 400
    if len(username) < 3:
        return jsonify({"msg": "username is too short"}), 400
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"msg": "The username is already in use"}), 409
    new_user = User(
        username=username,
    )

    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user added successfully!", "id": new_user.id}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    errors = user_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    auth_user = User.query.filter_by(username=data['username']).first()

    if auth_user is not None and auth_user.check_password(data['password']):
        access_token = create_access_token(identity=auth_user.username)
        refresh_token = create_refresh_token(identity=auth_user.username)

        resp = jsonify({'login': True})
        resp.headers['X-ACCESS-TOKEN-CSRF'] = get_csrf_token(access_token)
        resp.headers['X-REFRESH-TOKEN-CSRF'] = get_csrf_token(refresh_token)
        # set_access_cookies(resp, access_token)
        # set_refresh_cookies(resp, refresh_token)
        resp.set_cookie('access_token_cookie', access_token,
                        samesite='None', secure=True)
        resp.set_cookie('refresh_token_cookie', refresh_token,
                        samesite='None', secure=True)
        return resp, 200
    else:
        return make_response(jsonify({'message': 'Invalid User.'}), 401)


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    csrf_token = get_csrf_token(access_token)
    resp = jsonify({'refresh': True})
    resp.headers["X-CSRF-TOKEN"] = csrf_token
    set_access_cookies(resp, access_token)
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


@jwt.token_in_blocklist_loader
def token_block(_jwt_header, jwt_data):
    if TokenBlocklist.query.filter_by(jti=jwt_data["jti"]).first():
        return True
    return False
