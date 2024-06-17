from extensions import db_session
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, get_jwt,
                                set_access_cookies, set_refresh_cookies, unset_jwt_cookies)
from flask import jsonify
from datetime import datetime, timezone
from ..models import User, UserSchema, TokenBlocklist
from ..validators import post_user_schema, login_user_schema
from api.error import InvalidAPIUsage
from .utils import validate_data, save_to_db


def signup_user(data):
    session = db_session()
    validate_data(post_user_schema, data)
    try:
        user = session.query(User).filter_by(username=data["username"], facility_id=data["facility_id"]).first()
        if user:
            return None
        new_user = User(**data)
        save_to_db(new_user, session)
        res = UserSchema().dump(new_user)
        return res
    except Exception as e:
        db_session.rollback()
        if "foreign key constraint" in str(e):
            raise InvalidAPIUsage("The facility does not exist.", 400)
        else:
            raise InvalidAPIUsage("An error occurred while saving the user.", 500)
    finally:
        session.close()


def login_user(data):
    session = db_session()
    try:
        validate_data(login_user_schema, data)
        auth_user = session.query(User).filter_by(username=data['username']).first()

        if auth_user is not None and auth_user.check_password(data['password']):
            access_token = create_access_token(identity=auth_user.user_id)
            refresh_token = create_refresh_token(identity=auth_user.user_id)
            resp = jsonify({'login': True})
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp
        else:
            raise InvalidAPIUsage('Invalid User.', 401)
    finally:
        session.close()


def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    resp = jsonify({'refresh': True})
    resp.set_cookie('access_token_cookie', '', expires=datetime(1970, 1, 1))
    resp.set_cookie('access_token_cookie', access_token,
                    samesite='None', secure=True)
    return resp


def logout_user():
    session = db_session()
    try:
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)
        new_block_token = TokenBlocklist(jti=jti, type=ttype, created_at=now)
        save_to_db(new_block_token, session)
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp
    except Exception as e:
        session.rollback()
        raise InvalidAPIUsage("An error occurred while logging out.", 500)
    finally:
        session.close()
