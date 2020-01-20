import hashlib
from flask import Blueprint
from flask_jwt_extended import create_access_token, get_jwt_claims, get_jwt_identity, jwt_required
from flask_restful import Api, Resource, marshal, reqparse
from ..toko.models import Toko, Barang, harga_bahan
from ..auth.models import User
from ..barang.models import Keranjang
from blueprints import db, app
# password Encription
from password_strength import PasswordPolicy
# Gmail Function
import gmail
# Gmail message text
from message import register_html

bp_toko = Blueprint('toko', __name__)
api = Api(bp_toko)


class RegisterTokoResource(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        user_id = claims['id']
        parser = reqparse.RequestParser()
        parser.add_argument('nama_toko', location='json', required=True)
        parser.add_argument('deskripsi', location='json', required=True)
        args = parser.parse_args()
        # GET USER_ID AND USER FULLNAME FROM USER
        user = User.query.get(user_id)
        if user.designer_status == False:
            user.designer_status = True
            db.session.add(user)
            toko = Toko(user.id, args['nama_toko'],
                        args['deskripsi'], user.username)
            db.session.add(toko)
            db.session.commit()
            # SEND EMAIL VIA GMAIL API
            signature = gmail.get_signature()
            message = register_html.message.format(user.full_name) + signature
            subject = "YOUR STORE : {} IS OFFICIALLY OPEN! (TEESIGNR)".format(
                args['nama_toko'])
            gmail.send_email("TEESIGNR", user.email, subject, message)
            return {"status": "register berhasil", "toko": marshal(toko, Toko.response_fields)}, 200, {'Content-type': 'application/json'}
        else:
            return {"status": "register gagal", "message": "kamu sudah punya toko"}, 400

    def options(self):
        return {}, 200


class TokoJualResource(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        user_id = claims['id']
        parser = reqparse.RequestParser()
        parser.add_argument('nama_barang', location='json', required=True)
        parser.add_argument('keuntungan', location='json', required=True)
        parser.add_argument('desain', location='json', required=True)
        parser.add_argument('jenis_bahan', location='json', required=True, help='bahan tidak terdaftar', choices=(
            'Combed 20s', 'Combed 24s', 'Combed 30s', 'Combed 40s', 'Bamboo 30s', 'Modal 30s', 'Supima 30s'))
        parser.add_argument('deskripsi', location='json', required=True)
        args = parser.parse_args()
        # check if user already have toko
        user = User.query.get(user_id)
        if user.designer_status == True:
            toko = Toko.query.filter_by(user_id=user_id).first()
            toko_id = toko.id
            harga = int(args['keuntungan']) + harga_bahan[args['jenis_bahan']]
            barang = Barang(toko_id, args['nama_barang'], "Rp. {}".format(
                harga), harga, args['deskripsi'], args['jenis_bahan'], args['desain'])
            db.session.add(barang)
            db.session.commit()
            return {"status": "menambah jualan berhasil", "barang": marshal(barang, Barang.response_fields)}, 200, {'Content-type': 'application/json'}
        else:
            return {"status": "menambah jualan gagal", "message": "anda belum mempunyai toko"}, 400

    def options(self):
        return {}, 200


class CekTokoResource(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        user_id = claims['id']
        user = User.query.get(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='json', default=1)
        parser.add_argument('rp', type=int, location='json', default=12)
        parser.add_argument('harga minimal', type=int, location='json')
        parser.add_argument('harga maksimal', type=int, location='json')
        parser.add_argument('jenis bahan', location='json', help='bahan tidak terdaftar', choices=(
            'Combed 20s', 'Combed 24s', 'Combed 30s', 'Combed 40s', 'Bamboo 30s', 'Modal 30s', 'Supima 30s'))
        parser.add_argument('orderby', location='json', help='invalid orderby value', choices=(
            'terjual', 'id', 'harga'), default='terjual')
        parser.add_argument('sort', location='json', help='invalid sort value', choices=(
            'desc', 'asc'), default='desc')
        args = parser.parse_args()
        # Menentukan offset buat limit hasil pencarian
        offset = (args['p'] * args['rp']) - args['rp']
        # Check Toko dan Return hasil
        if user.designer_status == True:
            toko = Toko.query.filter_by(user_id=user_id).first()
            keuntungan = "Rp. {}".format(toko.keuntungan)
            marshal_toko = marshal(toko, Toko.response_fields)
            list_barang = Barang.query.filter_by(toko_id=toko.id)
            # Check masing masing filter
            # Check filter harga
            if args['harga minimal'] is not None:
                list_barang = list_barang.filter(
                    Barang.harga_int >= args['harga minimal'])
            if args['harga maksimal'] is not None:
                list_barang = list_barang.filter(
                    Barang.harga_int <= args['harga maksimal'])
            # Check filter jenis bahan
            if args['jenis bahan'] is not None:
                list_barang = list_barang.filter_by(bahan=args['jenis bahan'])
            # Check sort and orderby
            if args['orderby'] is not None:
                if args['orderby'] == 'terjual':
                    if args['sort'] == 'desc':
                        list_barang = list_barang.order_by(
                            Barang.terjual.desc())
                    else:
                        list_barang = list_barang.order_by(Barang.terjual)
                if args['orderby'] == 'harga':
                    if args['sort'] == 'desc':
                        list_barang = list_barang.order_by(
                            Barang.harga_int.desc())
                    else:
                        list_barang = list_barang.order_by(Barang.harga_int)
                else:
                    if args['sort'] == 'desc':
                        list_barang = list_barang.order_by(Barang.id.desc())
                    else:
                        list_barang = list_barang.order_by(Barang.id)
            # Limit Query
            barang_limit = list_barang.limit(args['rp']).offset(offset)

            barang_dijual = []
            for barang in barang_limit:
                marshal_barang = marshal(barang, Barang.response_fields)
                barang_dijual.append(marshal_barang)
            marshal_toko['keuntungan'] = keuntungan
            marshal_toko['daftar jualan'] = barang_dijual
            return marshal_toko, 200, {'Content-type': 'application/json'}
        else:
            return {"status": "not found", "message": "anda belum mempunyai toko"}, 400

    def options(self):
        return {}, 200


class ListTokoResource(Resource):
    def get(self):
        qry_toko = Toko.query
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=3)
        parser.add_argument('search', location='args')
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=(
            'popularitas', 'id'), default='popularitas')
        parser.add_argument('sort', location='args', help='invalid sort value', choices=(
            'desc', 'asc'), default='desc')
        args = parser.parse_args()
        # Menentukan offset buat limit hasil pencarian
        offset = (args['p'] * args['rp']) - args['rp']
        # Filter search
        if args['search'] is not None:
            search = "%{}%".format(args['search'])
            qry_toko = qry_toko.filter(Toko.nama.like(
                search) | Toko.deskripsi.like(search))
        # Orderby
        if args['orderby'] is not None:
            if args['orderby'] == "popularitas":
                if args['sort'] == 'desc':
                    qry_toko = qry_toko.order_by(Toko.popularitas.desc())
                else:
                    qry_toko = qry_toko.order_by(Toko.popularitas)
            else:
                if args['sort'] == 'desc':
                    qry_toko = qry_toko.order_by(Toko.id.desc())
                else:
                    qry_toko = qry_toko.order_by(Toko.id)
        toko_limit = qry_toko.limit(args['rp']).offset(offset)
        daftar_toko = []
        for toko in toko_limit:
            marshal_toko = marshal(toko, Toko.response_fields)
            barang_toko = Barang.query.filter_by(toko_id=toko.id)
            barang_populer = ""
            for barang in barang_toko:
                marshal_barang = marshal(barang, Barang.response_fields)
                if barang_populer == "":
                    barang_populer = marshal_barang
                elif barang_populer['terjual'] < marshal_barang['terjual']:
                    barang_populer = marshal_barang
            marshal_toko['barang_populer'] = barang_populer
            daftar_toko.append(marshal_toko)
        return daftar_toko, 200, {'Content-Type': 'application/json'}


class TokoIdResource(Resource):
    def get(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=12)
        parser.add_argument('harga minimal', type=int, location='args')
        parser.add_argument('harga maksimal', type=int, location='args')
        parser.add_argument('jenis bahan', location='args', help='bahan tidak terdaftar', choices=(
            'Combed 20s', 'Combed 24s', 'Combed 30s', 'Combed 40s', 'Bamboo 30s', 'Modal 30s', 'Supima 30s'))
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=(
            'terjual', 'id', 'harga'))
        parser.add_argument('sort', location='args',
                            help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()
        # Menentukan offset buat limit hasil pencarian
        offset = (args['p'] * args['rp']) - args['rp']
        # Check Toko dan Return hasil
        toko = Toko.query.filter_by(id=id).first()
        marshal_toko = marshal(toko, Toko.response_fields)
        list_barang = Barang.query.filter_by(toko_id=toko.id)
        # Check masing masing filter
        # Check filter harga
        if args['harga minimal'] is not None:
            list_barang = list_barang.filter(
                Barang.harga_int >= args['harga minimal'])
        if args['harga maksimal'] is not None:
            list_barang = list_barang.filter(
                Barang.harga_int <= args['harga maksimal'])
        # Check filter jenis bahan
        if args['jenis bahan'] is not None:
            list_barang = list_barang.filter_by(bahan=args['jenis bahan'])
        # Check sort and orderby
        if args['orderby'] is not None:
            if args['orderby'] == 'terjual':
                if args['sort'] == 'desc':
                    list_barang = list_barang.order_by(Barang.terjual.desc())
                else:
                    list_barang = list_barang.order_by(Barang.terjual)
            if args['orderby'] == 'harga':
                if args['sort'] == 'desc':
                    list_barang = list_barang.order_by(Barang.harga_int.desc())
                else:
                    list_barang = list_barang.order_by(Barang.harga_int)
            else:
                if args['sort'] == 'desc':
                    list_barang = list_barang.order_by(Barang.id.desc())
                else:
                    list_barang = list_barang.order_by(Barang.id)
        # Limit Query
        barang_limit = list_barang.limit(args['rp']).offset(offset)
        barang_dijual = []
        for barang in barang_limit:
            marshal_barang = marshal(barang, Barang.response_fields)
            barang_dijual.append(marshal_barang)
        marshal_toko['daftar jualan'] = barang_dijual
        return marshal_toko, 200, {'Content-type': 'application/json'}


class EditTokoResource(Resource):
    # Update deskripsi dan nama toko
    @jwt_required
    def put(self):
        claims = get_jwt_claims()
        user_id = claims['id']
        toko = Toko.query.filter_by(user_id=user_id).first()
        parser = reqparse.RequestParser()
        parser.add_argument('nama_toko', location='json')
        parser.add_argument('deskripsi', location='json')
        args = parser.parse_args()
        if toko is not None:
            if args['nama_toko'] is not None:
                toko.nama = args['nama_toko']
            if args['deskripsi'] is not None:
                toko.deskripsi = args['deskripsi']
            db.session.add(toko)
            db.session.commit()
            return {"status": "edit sukses", "detail toko": marshal(toko, Toko.response_fields)}, 200, {'Content-Type': 'application/json'}
        else:
            return {"status": "kamu belum punya toko"}, 400

    def options(self):
        return {}, 200

    # Hapus barang jualan
    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('barang_id', type=int,
                            location='json', required=True)
        args = parser.parse_args()
        claims = get_jwt_claims()
        user_id = claims['id']
        toko = Toko.query.filter_by(user_id=user_id).first()
        barang = Barang.query.get(args['barang_id'])
        if barang is not None:
            if barang.toko_id == toko.id:
                # Menghapus barang yang ada di keranjang sebelum menghapus barang di toko
                list_keranjang = Keranjang.query.filter_by(
                    barang_id=args['barang_id'])
                for keranjang in list_keranjang:
                    db.session.delete(keranjang)
                    db.session.commit()
                db.session.delete(barang)
                db.session.commit()
                return {"status": "barang berhasil dihapus"}, 200, {'Content-Type': 'application/json'}
            else:
                return {"status": "gagal", "message": "barang tidak ditemukan"}, 400
        else:
            return {"status": "barang tidak ditemukan"}, 404

    def options(self):
        return {}, 200


api.add_resource(RegisterTokoResource, '/register')
api.add_resource(TokoJualResource, '/jual')
api.add_resource(EditTokoResource, '/edit')
api.add_resource(CekTokoResource, '/cek')
api.add_resource(ListTokoResource, '')
api.add_resource(TokoIdResource, '/<id>')
