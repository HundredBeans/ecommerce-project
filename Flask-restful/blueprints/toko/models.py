from blueprints import db
from flask_restful import fields

harga_bahan = {
    "Combed 20s":98000,
    "Combed 24s":100000,
    "Combed 30s":103500,
    "Combed 40s":127000,
    "Bamboo 30s":115000,
    "Modal 30s":119000,
    "Supima 30s":178000
}

class Toko(db.Model):
    __tablename__ = "toko"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) #diambil dari data claims
    nama = db.Column(db.String(191), unique=True, nullable=False)
    deskripsi = db.Column(db.String(1000), nullable=False)
    pemilik = db.Column(db.String(191), db.ForeignKey("user.username"), nullable=False) #diambil dari data claims
    popularitas = db.Column(db.Integer, nullable=False, default=0)
    keuntungan = db.Column(db.Integer, nullable=False, default=0) #diupdate setiap kali ada yang beli

    response_fields = {
        'id':fields.Integer,
        'user_id':fields.Integer,
        'nama':fields.String,
        'deskripsi':fields.String,
        'pemilik':fields.String,
        'popularitas':fields.Integer
    }

    def __init__(self, user_id, nama, deskripsi, pemilik):
        self.user_id = user_id
        self.nama = nama
        self.deskripsi = deskripsi
        self.pemilik = pemilik

# TABLE BARANG
class Barang(db.Model):
    __tablename__ = "barang"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    toko_id = db.Column(db.Integer, db.ForeignKey("toko.id"), nullable=False)
    nama = db.Column(db.String(255), nullable=False)
    harga = db.Column(db.String(255), nullable=False)
    harga_int = db.Column(db.Integer, nullable=False)
    deskripsi = db.Column(db.String(1000), nullable=False)
    bahan = db.Column(db.String(255), nullable=False)
    gambar = db.Column(db.String(1000), nullable=False)
    terjual = db.Column(db.Integer, nullable=False, default=0)

    response_fields = {
        'id':fields.Integer,
        'toko_id':fields.Integer,
        'nama':fields.String,
        'harga':fields.String,
        'deskripsi':fields.String,
        'bahan':fields.String,
        'gambar':fields.String,
        'terjual':fields.Integer
    }

    def __init__(self, toko_id, nama, harga, harga_int, deskripsi, bahan, gambar):
        self.harga = harga
        self.toko_id = toko_id
        self.nama = nama
        self.harga_int = harga_int
        self.deskripsi = deskripsi
        self.bahan = bahan
        self.gambar = gambar
