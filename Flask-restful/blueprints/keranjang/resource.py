import hashlib
import requests
import json
from flask import Blueprint
from flask_jwt_extended import create_access_token, get_jwt_claims, get_jwt_identity, jwt_required
from flask_restful import Api, Resource, marshal, reqparse
from ..toko.models import Toko, Barang, harga_bahan
from ..auth.models import User
from ..barang.models import Keranjang
from blueprints import db, app

bp_keranjang = Blueprint('keranjang', __name__)
api = Api(bp_keranjang)


class ListKeranjangResource(Resource):
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('search', location='args')
        parser.add_argument('orderby', location='args',
                            help='invalid orderby value', choices=('harga', 'id'))
        parser.add_argument('sort', location='args',
                            help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()
        # Menentukan offset buat limit hasil pencarian
        offset = (args['p'] * args['rp']) - args['rp']
        # Filter keranjang by user_id from jwt claims
        claims = get_jwt_claims()
        user_id = claims['id']
        qry_keranjang = Keranjang.query.filter_by(user_id=user_id)
        qry_keranjang = qry_keranjang.filter_by(checkout_status=False)
        if args['search'] is not None:
            search = "%{}%".format(args['search'])
            qry_keranjang = qry_keranjang.filter(
                Keranjang.nama_barang.like(search))
        if args['orderby'] is not None:
            if args['orderby'] == "harga":
                if args['sort'] == 'desc':
                    qry_keranjang = qry_keranjang.order_by(
                        (Keranjang.harga_barang_int*Keranjang.jumlah).desc())
                else:
                    qry_keranjang = qry_keranjang.order_by(
                        (Keranjang.harga_barang_int*Keranjang.jumlah))
            else:
                if args['sort'] == 'desc':
                    qry_keranjang = qry_keranjang.order_by(Keranjang.id.desc())
                else:
                    qry_keranjang = qry_keranjang.order_by(Keranjang.id)
        keranjang_limit = qry_keranjang.limit(args['rp']).offset(offset)
        list_keranjang = []
        for keranjang in keranjang_limit:
            keranjang_marshal = marshal(keranjang, Keranjang.response_fields)
            total_harga = keranjang.harga_barang_int*keranjang.jumlah
            keranjang_marshal['total_harga'] = total_harga
            list_keranjang.append(keranjang_marshal)
        return list_keranjang, 200, {'Content-type': 'application/json'}

    @jwt_required
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json', required=True)
        parser.add_argument('jumlah', type=int, location='json')
        parser.add_argument('ukuran', location='json')
        args = parser.parse_args()
        claims = get_jwt_claims()
        user_id = claims['id']
        # get keranjang by id
        keranjang = Keranjang.query.get(args['id'])
        if keranjang is not None and keranjang.user_id == user_id:
            # edit jumlah
            if args['jumlah'] is not None:
                keranjang.jumlah = args['jumlah']
                total_harga = keranjang.harga_barang_int*keranjang.jumlah
            # edit ukuran
            if args['ukuran'] is not None:
                keranjang.ukuran = args['ukuran']
            db.session.add(keranjang)
            db.session.commit()
            keranjang_marshal = marshal(keranjang, Keranjang.response_fields)
            keranjang_marshal['Total Harga'] = total_harga
            return {"status": "edit keranjang berhasil", "detail": keranjang_marshal}, 200, {'Content-type': 'application/json'}
        else:
            return {"status": "edit keranjang gagal"}, 400

    # Checkout keranjang
    # Tambah API untuk ngirim email ke pendaftar atau Telegram
    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        # id keranjang yang mau checkout (berupa list)
        # parser.add_argument('id', type=list, location='json', required=True)
        args = parser.parse_args()
        claims = get_jwt_claims()
        user_id = claims['id']
        list_checkout = []
        total_harga = 0
        list_keranjang = Keranjang.query.all()
        for keranjang in list_keranjang:
            # check jika keranjang tersebut punya dia
            if keranjang.user_id == user_id and keranjang.checkout_status == False:
                keranjang.checkout_status = True
                # db.session.add(keranjang)
                db.session.commit()
                harga = keranjang.harga_barang_int * keranjang.jumlah
                total_harga += harga
                total = "Rp. {}".format(harga)
                keranjang_marshal = marshal(
                    keranjang, Keranjang.response_fields)
                keranjang_marshal['total harga'] = total
                list_checkout.append(keranjang_marshal)
        if len(list_checkout) > 0:
            return {"status": "silahkan lakukan konfirmasi pemesanan", "total harga": total_harga, "detail": list_checkout}, 200, {'Content-type': 'application/json'}
        else:
            return {"status": "checkout gagal"}, 403

    # Menghapus Keranjang
    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        # id keranjang yang mau dihapus (berupa list)
        parser.add_argument('id', type=int, location='json')
        args = parser.parse_args()
        claims = get_jwt_claims()
        user_id = claims['id']
        list_keranjang = Keranjang.query.filter_by(user_id=user_id)
        hapus_counter = 0
        if args['id'] is None or args['id'] == 0:
            for keranjang in list_keranjang:
                if keranjang.checkout_status == False:
                    db.session.delete(keranjang)
                    db.session.commit()
            return {"status": "semua barang di keranjang berhasil dihapus"}, 200, {'Content-type': 'application/json'}
        else:
            for keranjang in list_keranjang:
                if keranjang.id == args['id'] and keranjang.checkout_status == False:
                    hapus_counter += 1
                    db.session.delete(keranjang)
                    db.session.commit()
            return {"status": "{} barang di keranjang berhasil dihapus".format(hapus_counter)}, 200, {'Content-type': 'application/json'}

    def options(self):
        return {}, 200


api.add_resource(ListKeranjangResource, '')
