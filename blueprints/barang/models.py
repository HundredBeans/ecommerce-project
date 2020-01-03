from blueprints import db
from flask_restful import fields

class Keranjang(db.Model):
    __tablename__ = "keranjang"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barang_id = db.Column(db.Integer, db.ForeignKey("barang.id"), nullable=False)
    nama_barang = db.Column(db.String(255), nullable=False)
    harga_barang_int = db.Column(db.Integer, nullable=False)
    harga_barang = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    ukuran = db.Column(db.String(255), nullable=False)
    checkout_status = db.Column(db.Boolean, default=False)

    response_fields = {
        'id':fields.Integer,
        'barang_id':fields.Integer,
        'nama_barang':fields.String,
        'harga_barang_int':fields.Integer,
        'harga_barang':fields.String,
        'user_id':fields.Integer,
        'jumlah':fields.Integer,
        'ukuran':fields.String
    }

    def __init__(self, barang_id, nama_barang, harga_barang_int, harga_barang, user_id, jumlah, ukuran):
        self.barang_id = barang_id
        self.nama_barang = nama_barang
        self.harga_barang_int = harga_barang_int
        self.harga_barang = harga_barang
        self.user_id = user_id
        self.jumlah = jumlah
        self.ukuran = ukuran