from blueprints import db
from flask_restful import fields
from datetime import datetime

class DetailPemesanan(db.Model):
    __tablename__ = "detail-pemesanan"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    nama_penerima = db.Column(db.String(255), nullable=False)
    no_telepon = db.Column(db.String(255), nullable=False)
    alamat_penerima = db.Column(db.String(1000), nullable=False)
    metode_pembayaran = db.Column(db.String(255), nullable=False)

    response_fields = {
        'id':fields.Integer,
        'user_id':fields.Integer,
        'nama_penerima':fields.String,
        'no_telepon':fields.String,
        'alamat_penerima':fields.String,
        'metode_pembayaran':fields.String
    }

    def __init__(self, user_id, nama_penerima, no_telepon, alamat_penerima, metode_pembayaran):
        self.user_id = user_id
        self.nama_penerima = nama_penerima
        self.no_telepon = no_telepon
        self.alamat_penerima = alamat_penerima
        self.metode_pembayaran = metode_pembayaran

class RiwayatPemesanan(db.Model):
    # Isinya berupa data yang mau dikirimkan setelah checkout keranjang ke konfirmasi pemesanan
    __tablename__ = "riwayat-pemesanan"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barang_id = db.Column(db.Integer, nullable=False)
    nama_barang = db.Column(db.String(255), nullable=False)
    harga_barang = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    ukuran = db.Column(db.String(255), nullable=False)
    id_pemesanan = db.Column(db.Integer, db.ForeignKey("detail-pemesanan.id"), nullable=False)
    total_harga = db.Column(db.String(255), nullable=False)
    total_harga_int = db.Column(db.Integer, nullable=False)
    waktu_pemesanan = db.Column(db.DateTime, default=datetime.now())

    def __init__(
        self, barang_id, nama_barang, harga_barang, user_id, jumlah, ukuran, 
        id_pemesanan, total_harga, total_harga_int
    ):
        self.barang_id = barang_id
        self.nama_barang = nama_barang
        self.harga_barang = harga_barang
        self.user_id = user_id
        self.jumlah = jumlah
        self.ukuran = ukuran
        self.id_pemesanan = id_pemesanan
        self.total_harga = total_harga
        self.total_harga_int = total_harga_int

    response_fields = {
        'id':fields.Integer,
        'barang_id':fields.Integer,
        'nama_barang':fields.String,
        'harga_barang':fields.String,
        'user_id':fields.Integer,
        'jumlah':fields.Integer,
        'ukuran':fields.String,
        'id_pemesanan':fields.Integer,
        'total_harga':fields.String,
        'total_harga_int':fields.Integer,
        'waktu_pemesanan':fields.DateTime
    }
