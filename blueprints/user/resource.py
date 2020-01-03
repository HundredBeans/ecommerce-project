import hashlib
from flask import Blueprint
from flask_jwt_extended import create_access_token, get_jwt_claims, get_jwt_identity, jwt_required
from flask_restful import Api, Resource, marshal, reqparse
from ..toko.models import Toko, Barang, harga_bahan
from ..auth.models import User
from ..barang.models import Keranjang
from blueprints import db, app
#password Encription
from password_strength import PasswordPolicy

bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class UserInfoResource(Resource):
    @jwt_required
    def get(self):
        pass

class UserEditResource(Resource):
    @jwt_required
    def patch(self):
        policy = PasswordPolicy.from_names(
            length = 6
        )
        parser = reqparse.RequestParser()
        parser.add_argument('old_password', location='json', required=True)
        parser.add_argument('new_password', location='json', required=True)
        args = parser.parse_args()
        claims = get_jwt_claims()
        user_id = claims['id']
        user = User.query.get(user_id)
        hashed_pass_old = hashlib.md5(args['old_password'].encode()).hexdigest()
        validation = policy.test(args['new_password'])
        if hashed_pass_old == user.password:
            if validation == []:
                hashed_pass_new = hashlib.md5(args['new_password'].encode()).hexdigest()
                user.password = hashed_pass_new
                db.session.add(user)
                db.session.commit()
                return {"status":"password berhasil diubah"}, 200, {'Content-Type': 'application/json'}
            else:
                return {"status":"gagal", "message":"password tidak valid"}, 400, {"Content-type":"application/json"}
        else:
            return {"status":"gagal", "message":"password salah"}, 401


api.add_resource(UserInfoResource, '')
api.add_resource(UserEditResource, '/edit')