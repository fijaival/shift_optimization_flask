from api.v1.models import User, TokenBlocklist
from api.v1.error import InvalidAPIUsage
from functools import wraps  # デコレータ作成用
from flask_jwt_extended import (
    JWTManager, verify_jwt_in_request, get_jwt,
)
from flask_jwt_extended import JWTManager
jwt = JWTManager()

'''以下で、JWTの挙動をデフォルトから変更する(エラーのフォーマットを変えるなど)'''
# アクセストークンに、権限情報も含めるようにする


@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.filter_by(user_id=identity).first()
    return {
        'user_id': identity,
        'is_admin': user.is_admin
    }

# トークンの有効期限切れ時の挙動


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    token_type = jwt_payload['type']
    if token_type == 'access':
        raise InvalidAPIUsage("Access token has expired", 401)
    else:
        raise InvalidAPIUsage("Refresh token has expired", 401)

# 無効な形式のトークン時の挙動


@jwt.invalid_token_loader
def my_invalid_token_callback(error_string):
    raise InvalidAPIUsage(error_string, 401)

# 認証エラー時の挙動


@jwt.unauthorized_loader
def my_unauthorized_callback(error_string):
    raise InvalidAPIUsage(error_string, 401)


@jwt.token_in_blocklist_loader
def token_block(jwt_header, jwt_payload):
    if TokenBlocklist.query.filter_by(jti=jwt_payload["jti"]).first():
        return True
    return False


'''アクセス制限用にデコレータを作成する'''
# 管理者のみアクセスできるエンドポイント


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()  # 通常のトークン認証
        claims = get_jwt()
        if claims['is_admin'] != 1:  # カスタマイズした権限情報の確認
            raise InvalidAPIUsage("Admins only", 403)
        else:
            return fn(*args, **kwargs)
    return wrapper
