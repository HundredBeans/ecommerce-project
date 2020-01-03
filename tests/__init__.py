import pytest, logging, json, hashlib
from blueprints import app, db
from app import cache
from flask import request
from blueprints.toko.models import Toko, Barang
from blueprints.auth.models import User
from blueprints.barang.models import Keranjang
from blueprints.checkout.models import DetailPemesanan, RiwayatPemesanan

def reset_db():
    db.drop_all()
    db.create_all()
    password = hashlib.md5("rahasia123".encode()).hexdigest()
    user = User("Mohammad Daffa", "daffa@alterra.id", "Fadafuq", password)
    db.session.add(user)
    db.session.commit()
    toko = Toko(1, "Test1", "Deskripsi toko test1", "Fadafuq")
    db.session.add(toko)
    db.session.commit()
    user = User.query.get(1)
    user.designer_status = True
    db.session.commit()
    barang = Barang(1, "Barang1", "Rp. 150000", 150000, "Deskripsi barang1", "Combed 30s", "https://s0.bukalapak.com/img/0347408453/w-1000/Kaos_Indonesia_Baju_Distro_Timnas_Lambang_Gambar_Timnas_Garu.jpg")
    db.session.add(barang)
    db.session.commit()
    user = User("Saipul Zuhair", "youdontsayhuman@gmail.com", "PigeonHole", password)
    db.session.add(user)
    db.session.commit()
    keranjang = Keranjang(1, "Barang1", 150000, "Rp. 150000", 1, 1, "XL")
    db.session.add(keranjang)
    db.session.commit()
    user = User("Bukan Dobleh", "m.daffa100@yahoo.com", "bukanDobleh", password)
    db.session.add(user)
    db.session.commit()
    toko = Toko(3, "Test2", "Deskripsi toko test2", "bukanDobleh")
    db.session.add(toko)
    db.session.commit()
    barang = Barang(2, "Barang2", "Rp. 150000", 150000, "Deskripsi barang2", "Combed 30s", "https://s0.bukalapak.com/img/0347408453/w-1000/Kaos_Indonesia_Baju_Distro_Timnas_Lambang_Gambar_Timnas_Garu.jpg")
    db.session.add(barang)
    db.session.commit()

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token(punya_toko=False):
    if punya_toko:
        cachename = 'test-punya-toko-token'
        data = {
            'email': 'daffa@alterra.id',
            'password': 'rahasia123'
        }
    else:
        cachename = 'test-token'
        data = {
            'email': 'youdontsayhuman@gmail.com',
            'password': 'rahasia123'
        }
    token = cache.get(cachename)
    if token is None:
    #prepare request input
        #do request
        req = call_client(request)
        res = req.post('/auth/login', json = data)

        #store response
        res_json = json.loads(res.data)
        logging.warning('RESULT : %s', res_json)

        ## assert / compare with expected result
        assert res.status_code == 200
        ## save token into cache
        cache.set(cachename, res_json['token'], timeout=60)
        ## return, because it useful for other test
        return res_json['token']
    else:
        return token
