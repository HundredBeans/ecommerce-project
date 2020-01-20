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

bp_barang = Blueprint('barang', __name__)
api = Api(bp_barang)


class ListBarangResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=12)
        parser.add_argument('search', location='args')
        parser.add_argument('harga_minimal', type=int, location='args')
        parser.add_argument('harga_maksimal', type=int, location='args')
        parser.add_argument('jenis_bahan', location='args', help='bahan tidak terdaftar', choices=(
            'Combed 20s', 'Combed 24s', 'Combed 30s', 'Combed 40s', 'Bamboo 30s', 'Modal 30s', 'Supima 30s'))
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=(
            'terjual', 'id', 'harga'))
        parser.add_argument('sort', location='args',
                            help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()
        # Menentukan offset buat limit hasil pencarian
        offset = (args['p'] * args['rp']) - args['rp']
        # Initiate query barang
        qry_barang = Barang.query
        # Filter search
        if args['search'] is not None:
            search = "%{}%".format(args['search'])
            qry_barang = qry_barang.filter(Barang.nama.like(
                search) | Barang.deskripsi.like(search))
        # Filter harga
        if args['harga_minimal'] is not None:
            qry_barang = qry_barang.filter(
                Barang.harga_int >= args['harga_minimal'])
        if args['harga_maksimal'] is not None:
            qry_barang = qry_barang.filter(
                Barang.harga_int <= args['harga_maksimal'])
        # Filter jenis bahan
        if args['jenis_bahan'] is not None:
            qry_barang = qry_barang.filter_by(bahan=args['jenis_bahan'])
        # Orderby
        if args['orderby'] is not None:
            if args['orderby'] == 'terjual':
                if args['sort'] == 'desc':
                    qry_barang = qry_barang.order_by(Barang.terjual.desc())
                else:
                    qry_barang = qry_barang.order_by(Barang.terjual)
            if args['orderby'] == 'harga':
                if args['sort'] == 'desc':
                    qry_barang = qry_barang.order_by(Barang.harga_int.desc())
                else:
                    qry_barang = qry_barang.order_by(Barang.harga_int)
            else:
                if args['sort'] == 'desc':
                    qry_barang = qry_barang.order_by(Barang.id.desc())
                else:
                    qry_barang = qry_barang.order_by(Barang.id)
        # Limit query (pagination)
        barang_limit = qry_barang.limit(args['rp']).offset(offset)
        list_barang = []
        for barang in barang_limit:
            marshal_barang = marshal(barang, Barang.response_fields)
            list_barang.append(marshal_barang)
        return list_barang, 200, {'Content-type': 'application/json'}


class BarangIdResource(Resource):
    def get(self, id):
        barang = Barang.query.get(id)
        if barang is not None:
            toko = Toko.query.get(barang.toko_id)
            penjual = toko.nama
            barang_marshal = marshal(barang, Barang.response_fields)
            barang_marshal['penjual'] = penjual
            return barang_marshal, 200, {'Content-type': 'application/json'}
        else:
            return {"status": "not found"}, 404

    # Menambah barang ke keranjang
    @jwt_required
    def put(self, id):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('jumlah', type=int, location='json', default=1)
        parser.add_argument('ukuran', location='json', required=True)
        args = parser.parse_args()
        # Properti Keranjang didapat dari query barang dan user
        user_id = claims['id']
        barang = Barang.query.get(id)
        barang_id = barang.id
        nama_barang = barang.nama
        harga_barang_int = barang.harga_int
        harga_barang = barang.harga
        ukuran = args['ukuran']
        jumlah = args['jumlah']
        total_harga = "Rp. {}".format(jumlah * harga_barang_int)
        keranjang = Keranjang(
            barang_id, nama_barang, harga_barang_int, harga_barang, user_id, jumlah, ukuran)
        db.session.add(keranjang)
        db.session.commit()
        keranjang_marshal = marshal(keranjang, Keranjang.response_fields)
        keranjang_marshal['Total Harga'] = total_harga
        return {"status": "berhasil ditambah ke keranjang", "detail": keranjang_marshal}, 200, {'Content-type': 'application/json'}

    # Beli barang seolah-olah tanpa masuk keranjang dengan mengubah checkout_status menjadi True
    @jwt_required
    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('jumlah', type=int, location='json', default=1)
        parser.add_argument('ukuran', location='json', required=True)
        args = parser.parse_args()
        claims = get_jwt_claims()
        # Properti Keranjang didapat dari query barang dan user
        user_id = claims['id']
        barang = Barang.query.get(id)
        barang_id = barang.id
        nama_barang = barang.nama
        harga_barang_int = barang.harga_int
        harga_barang = barang.harga
        ukuran = args['ukuran']
        jumlah = args['jumlah']
        total_harga_int = jumlah * harga_barang_int
        total_harga = "Rp. {}".format(total_harga_int)
        keranjang = Keranjang(
            barang_id, nama_barang, harga_barang_int, harga_barang, user_id, jumlah, ukuran)
        keranjang.checkout_status = True
        db.session.add(keranjang)
        db.session.commit()
        keranjang_marshal = marshal(keranjang, Keranjang.response_fields)
        keranjang_marshal['total harga'] = total_harga
        return {"status": "silahkan lakukan konfirmasi pemesanan", "total harga": total_harga_int, "detail": keranjang_marshal}, 200, {'Content-type': 'application/json'}

    def options(self, id):
        return {}, 200


api.add_resource(ListBarangResource, '')
api.add_resource(BarangIdResource, '/<id>')
