import hashlib, requests, json
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
        parser.add_argument('p', type=int, location='json', default=1)
        parser.add_argument('rp', type=int, location='json', default=20)
        parser.add_argument('search', location='json')
        parser.add_argument('orderby', location='json', help='invalid orderby value', choices=('harga', 'id'))
        parser.add_argument('sort', location='json', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()
        # Menentukan offset buat limit hasil pencarian
        offset = (args['p'] * args['rp']) - args['rp']
        # Filter keranjang by user_id from jwt claims
        claims = get_jwt_claims()
        user_id = claims['id']
        qry_keranjang = Keranjang.query.filter_by(user_id=user_id)
        if args['search'] is not None:
            search = "%{}%".format(args['search'])
            qry_keranjang = qry_keranjang.filter(Keranjang.nama_barang.like(search))
        if args['orderby'] is not None:
            if args['orderby'] == "harga":
                if args['sort'] =='desc':
                    qry_keranjang = qry_keranjang.order_by((Keranjang.harga_barang_int*Keranjang.jumlah).desc())
                else:
                    qry_keranjang = qry_keranjang.order_by((Keranjang.harga_barang_int*Keranjang.jumlah))
            else:
                if args['sort'] =='desc':
                    qry_keranjang = qry_keranjang.order_by(Keranjang.id.desc())
                else:
                    qry_keranjang = qry_keranjang.order_by(Keranjang.id)
        keranjang_limit = qry_keranjang.limit(args['rp']).offset(offset)
        list_keranjang = []
        for keranjang in keranjang_limit:
            keranjang_marshal = marshal(keranjang, Keranjang.response_fields)
            total_harga = keranjang.harga_barang_int*keranjang.jumlah
            keranjang_marshal['Total Harga'] = total_harga
            list_keranjang.append(keranjang_marshal)
        return list_keranjang, 200, {'Content-type': 'application/json'}

    @jwt_required
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json', required=True)
        parser.add_argument('jumlah', type=int, location='json')
        parser.add_argument('ukuran', location='json')
        args = parser.parse_args()
        # get keranjang by id
        keranjang = Keranjang.query.get(args['id'])
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
        return {"status":"edit keranjang berhasil", "detail":keranjang_marshal}, 200, {'Content-type': 'application/json'}

api.add_resource(ListKeranjangResource, '')