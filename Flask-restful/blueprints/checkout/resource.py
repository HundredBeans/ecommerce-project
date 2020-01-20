import hashlib
import requests
import json
from flask import Blueprint
from flask_jwt_extended import create_access_token, get_jwt_claims, get_jwt_identity, jwt_required
from flask_restful import Api, Resource, marshal, reqparse
from ..toko.models import Toko, Barang, harga_bahan
from ..auth.models import User
from ..barang.models import Keranjang
from ..checkout.models import DetailPemesanan, RiwayatPemesanan
from blueprints import db, app
# Gmail Function
import gmail
# Gmail message text
from message import bought_html
from message import konfirmasi_html

bp_checkout = Blueprint('checkout', __name__)
api = Api(bp_checkout)


class ListCheckoutResource(Resource):
    # Konfirmasi Pemesanan
    # Nantinya dikombinasikan dengan E-Mail API
    @jwt_required
    def post(self):
        # Seharusnya mengambil value seperti total harga dari respond checkout keranjang (patch) dan beli barang
        claims = get_jwt_claims()
        user_id = claims['id']
        parser = reqparse.RequestParser()
        parser.add_argument('nama_penerima', location='json', required=True)
        parser.add_argument('no_telepon', location='json', required=True)
        parser.add_argument('alamat_penerima', location='json', required=True)
        parser.add_argument('metode_pembayaran',
                            location='json', required=True)
        args = parser.parse_args()
        detail_pemesanan = DetailPemesanan(
            user_id, args['nama_penerima'], args['no_telepon'], args['alamat_penerima'], args['metode_pembayaran'])
        db.session.add(detail_pemesanan)
        db.session.commit()
        marshal_detail_pemesanan = marshal(
            detail_pemesanan, DetailPemesanan.response_fields)
        # Bikin Properti untuk Riwayat Pemesanan
        # keranjang_id, barang_id, nama_barang, harga_barang, user_id, jumlah, ukuran,
        # id_pemesanan, total_harga, total_harga_int
        # Ambil semua data keranjang dengan checkout_status = True
        daftar_belanjaan = []
        list_keranjang = Keranjang.query.filter_by(user_id=user_id)
        total_belanja = 0
        for keranjang in list_keranjang:
            if keranjang.checkout_status == True:
                barang_id = keranjang.barang_id
                nama_barang = keranjang.nama_barang
                harga_barang = keranjang.harga_barang
                user_id = user_id
                jumlah = keranjang.jumlah
                ukuran = keranjang.ukuran
                id_pemesanan = detail_pemesanan.id
                total_harga = "Rp. {}".format(
                    keranjang.jumlah * keranjang.harga_barang_int)
                total_harga_int = keranjang.jumlah * keranjang.harga_barang_int
                pemesanan = RiwayatPemesanan(barang_id, nama_barang, harga_barang,
                                             user_id, jumlah, ukuran, id_pemesanan, total_harga, total_harga_int)
                # Menambah jumlah barang terjual di masing masing barang
                barang = Barang.query.get(barang_id)
                barang.terjual = barang.terjual + jumlah
                # Menambah popularitas senilai 5 di toko
                toko_id = barang.toko_id
                toko = Toko.query.get(toko_id)
                toko.popularitas = toko.popularitas + 5
                # Menambah keuntungan di toko
                untung = (keranjang.harga_barang_int -
                          harga_bahan[barang.bahan])*jumlah
                toko.keuntungan = toko.keuntungan + untung
                db.session.add(barang)
                db.session.add(toko)
                db.session.add(pemesanan)
                db.session.delete(keranjang)
                db.session.commit()
                total_belanja += total_harga_int
                pemesanan_marshal = marshal(
                    pemesanan, RiwayatPemesanan.response_fields)
                daftar_belanjaan.append(pemesanan_marshal)
                # Email si penjual / designer bahwa jualannya laku
                designer = User.query.get(toko.user_id)
                nama_designer = designer.full_name
                email_designer = designer.email
                signature = gmail.get_signature()
                message = bought_html.message.format(
                    nama_designer, nama_barang) + signature
                subject = "GREAT NEWS FROM TEESIGNR"
                gmail.send_email("teesignr@gmail.com",
                                 email_designer, subject, message)
        # Email si pembeli detail pemesanan
        pesanan_id = detail_pemesanan.id
        user = User.query.get(user_id)
        full_name = user.full_name
        total_harga_belanja = "Rp. {}".format(total_belanja)
        metode_pembayaran = args['metode_pembayaran']
        nama_penerima = args['nama_penerima']
        nomor_telepon = args['no_telepon']
        alamat_penerima = args['alamat_penerima']
        email_user = user.email
        signature = gmail.get_signature()
        message = konfirmasi_html.PesananEmail(full_name, pesanan_id, total_harga_belanja, metode_pembayaran,
                                               nama_penerima, nomor_telepon, alamat_penerima, daftar_belanjaan) + signature
        subject = "ORDER INFORMATION (TEESIGNR)"
        gmail.send_email("teesignr@gmail.com", email_user, subject, message)

        marshal_detail_pemesanan["total_belanja"] = "Rp. {}".format(
            total_belanja)
        marshal_detail_pemesanan["daftar_belanja"] = daftar_belanjaan
        return {"status": "checkout berhasil", "detail": marshal_detail_pemesanan}, 200, {'Content-type': 'application/json'}

    # List daftar pesanan yang sudah dicheckout
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        user_id = claims['id']
        list_keranjang = Keranjang.query.filter_by(user_id=user_id)
        list_belanjaan = []
        total_belanja = 0
        for keranjang in list_keranjang:
            if keranjang.checkout_status == True:
                harga_total = keranjang.jumlah * keranjang.harga_barang_int
                total_belanja = total_belanja + harga_total
                keranjang_marshal = marshal(
                    keranjang, Keranjang.response_fields)
                list_belanjaan.append(keranjang_marshal)
        return {"total_belanja": total_belanja, "list_belanjaan": list_belanjaan}, 200, {'Content-type': 'application/json'}

    # Cancel Pemesanan
    @jwt_required
    def delete(self):
        claims = get_jwt_claims()
        user_id = claims['id']
        list_keranjang = Keranjang.query.filter_by(user_id=user_id)
        for keranjang in list_keranjang:
            if keranjang.checkout_status == True:
                keranjang.checkout_status = False
                db.session.add(keranjang)
                db.session.commit()
        return {"status": "pesanan dibatalkan", "message": "barang dimasukkan ke keranjang"}, 200, {'Content-type': 'application/json'}

    def options(self):
        return {}, 200


api.add_resource(ListCheckoutResource, '')
