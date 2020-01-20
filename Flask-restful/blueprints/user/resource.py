import hashlib
from flask import Blueprint
from flask_jwt_extended import create_access_token, get_jwt_claims, get_jwt_identity, jwt_required
from flask_restful import Api, Resource, marshal, reqparse
from ..toko.models import Toko, Barang, harga_bahan
from ..auth.models import User
from ..barang.models import Keranjang
from ..checkout.models import RiwayatPemesanan
from blueprints import db, app
# password Encription
from password_strength import PasswordPolicy

bp_user = Blueprint('user', __name__)
api = Api(bp_user)


class UserInfoResource(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        user_id = claims['id']
        user = User.query.get(user_id)
        toko = Toko.query.filter_by(user_id=user_id).first()
        riwayat_pemesanan = RiwayatPemesanan.query.filter_by(user_id=user_id)
        marshal_user = marshal(user, User.response_fields)
        list_transaksi = []
        for transaksi in riwayat_pemesanan:
            marshal_transaksi = marshal(
                transaksi, RiwayatPemesanan.response_fields)
            list_transaksi.append(marshal_transaksi)
        if toko is not None:
            marshal_toko = marshal(toko, Toko.response_fields)
            keuntungan = "Rp. {}".format(toko.keuntungan)
            marshal_toko['keuntungan'] = keuntungan
            return {"info_user": marshal_user, "info_toko": marshal_toko, "riwayat_transaksi": list_transaksi}, 200, {'Content-Type': 'application/json'}
        else:
            return {"info_user": marshal_user, "riwayat_transaksi": list_transaksi}, 200, {'Content-Type': 'application/json'}

    def options(self):
        return {}, 200


class UserEditResource(Resource):
    @jwt_required
    def put(self):
        policy = PasswordPolicy.from_names(
            length=6
        )
        parser = reqparse.RequestParser()
        parser.add_argument('old_password', location='json', required=True)
        parser.add_argument('new_password', location='json', required=True)
        args = parser.parse_args()
        claims = get_jwt_claims()
        user_id = claims['id']
        user = User.query.get(user_id)
        hashed_pass_old = hashlib.md5(
            args['old_password'].encode()).hexdigest()
        validation = policy.test(args['new_password'])
        if hashed_pass_old == user.password:
            if validation == []:
                hashed_pass_new = hashlib.md5(
                    args['new_password'].encode()).hexdigest()
                user.password = hashed_pass_new
                db.session.add(user)
                db.session.commit()
                return {"status": "password berhasil diubah"}, 200, {'Content-Type': 'application/json'}
            else:
                return {"status": "gagal", "message": "password tidak valid"}, 400, {"Content-type": "application/json"}
        else:
            return {"status": "gagal", "message": "password salah"}, 401

    def options(self):
        return {}, 200


api.add_resource(UserInfoResource, '')
api.add_resource(UserEditResource, '/edit')
