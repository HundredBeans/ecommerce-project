import pytest, logging, json
from blueprints import app
from app import cache
from flask import request
from . import client, reset_db, create_token

class TestTokoCrud():
    reset_db()
    def test_register_toko_fail(self, client):
        token = create_token(True)
        data = {
            "nama_toko":"Test1",
            "deskripsi":"deksripsi toko Test1"
        }
        res = client.post('toko/register', json=data, headers={'Authorization' : 'Bearer ' + token})
        assert res.status_code == 400

    def test_jual_barang(self, client):
        token = create_token(True)
        data = {
            "nama_barang":"KAOS LENGAN PENDEK THE POPO -THE BEATLES BLACK-",
            "keuntungan":15000,
            "desain":"https://cf.shopee.co.id/file/71a6b24e95b35a915bb3cdcfe3cfc309_tn",
            "jenis_bahan":"Combed 30s",
            "deskripsi":"Material: Cotton Combed 30s. Produk Warna: Hitam"
        }
        res = client.post('toko/jual', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_jual_barang_fail(self, client):
        token = create_token(False)
        data = {
            "nama_barang":"KAOS LENGAN PENDEK THE POPO -THE BEATLES BLACK-",
            "keuntungan":15000,
            "desain":"https://cf.shopee.co.id/file/71a6b24e95b35a915bb3cdcfe3cfc309_tn",
            "jenis_bahan":"Combed 30s",
            "deskripsi":"Material: Cotton Combed 30s. Produk Warna: Hitam"
        }
        res = client.post('toko/jual', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_cek_toko_filter(self, client):
        token = create_token(True)
        data = {
            "p":1,
            "rp":20,
            "harga minimal":100000,
            "harga maksimal":1000000,
            "orderby":"harga",
            "sort":"desc"
        }
        res = client.get('toko/cek', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_cek_toko_filter2(self, client):
        token = create_token(True)
        data = {
            "p":1,
            "rp":20,
            "harga minimal":100000,
            "harga maksimal":1000000,
            "orderby":"harga",
            "sort":"asc"
        }
        res = client.get('toko/cek', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_cek_toko_sort(self, client):
        token = create_token(True)
        data = {
            "p":1,
            "rp":20,
            "harga minimal":100000,
            "harga maksimal":1000000,
            "orderby":"id",
            "sort":"desc"
        }
        res = client.get('toko/cek', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_cek_toko_sort2(self, client):
        token = create_token(True)
        data = {
            "p":1,
            "rp":20,
            "harga minimal":100000,
            "harga maksimal":1000000,
            "orderby":"id",
            "sort":"asc"
        }
        res = client.get('toko/cek', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_cek_toko_sort_terjual(self, client):
        token = create_token(True)
        data = {
            "p":1,
            "rp":20,
            "harga minimal":100000,
            "harga maksimal":1000000,
            "jenis bahan":"Combed 30s",
            "orderby":"terjual",
            "sort":"desc"
        }
        res = client.get('toko/cek', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_cek_toko_sort_terjual2(self, client):
        token = create_token(True)
        data = {
            "p":1,
            "rp":20,
            "harga minimal":100000,
            "harga maksimal":1000000,
            "jenis bahan":"Combed 30s",
            "orderby":"terjual",
            "sort":"asc"
        }
        res = client.get('toko/cek', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_cek_toko_fail(self, client):
        token = create_token(False)
        data = {
            "p":1,
            "rp":20,
            "harga minimal":100000,
            "harga maksimal":1000000,
            "orderby":"harga",
            "sort":"desc"
        }
        res = client.get('toko/cek', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_get_all_toko(self, client):
        res = client.get('toko')
        assert res.status_code == 200

    def test_get_toko_filter(self, client):
        data = {
            "p":1,
            "rp":20,
            "search":"",
            "orderby":"id",
            "sort":"desc"
        }
        res = client.get('toko', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_toko_filter2(self, client):
        data = {
            "p":1,
            "rp":20,
            "search":"",
            "orderby":"id",
            "sort":"asc"
        }
        res = client.get('toko', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_toko_filter3(self, client):
        data = {
            "p":1,
            "rp":20,
            "search":"",
            "orderby":"popularitas",
            "sort":"asc"
        }
        res = client.get('toko', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_toko_id(self, client):
        data = {
            "harga minimal":100000,
            "harga maksimal":1000000,
            "jenis bahan":"Combed 30s",
            "orderby":"terjual",
            "sort":"desc"
        }
        res = client.get('toko/1', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_toko_id_asc(self, client):
        data = {
            "harga minimal":100000,
            "harga maksimal":1000000,
            "jenis bahan":"Combed 30s",
            "orderby":"terjual",
            "sort":"asc"
        }
        res = client.get('toko/1', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_toko_id_asc_harga(self, client):
        data = {
            "harga minimal":100000,
            "harga maksimal":1000000,
            "jenis bahan":"Combed 30s",
            "orderby":"harga",
            "sort":"asc"
        }
        res = client.get('toko/1', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_toko_id_desc_harga(self, client):
        data = {
            "harga minimal":100000,
            "harga maksimal":1000000,
            "jenis bahan":"Combed 30s",
            "orderby":"harga",
            "sort":"desc"
        }
        res = client.get('toko/1', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_edit_toko(self, client):
        token = create_token(True)
        data = {
            "nama_toko":"baru",
            "deskripsi":"deskripsi baru"
        }
        res = client.put('toko/edit', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_edit_toko_fail(self, client):
        token = create_token(False)
        data = {
            "nama_toko":"baru",
            "deskripsi":"deskripsi baru"
        }
        res = client.put('toko/edit', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_delete_barang(self, client):
        token = create_token(True)
        data = {
            "barang_id":1
        }
        res = client.delete('toko/edit', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_barang_fail(self, client):
        token = create_token(True)
        data = {
            "barang_id":10
        }
        res = client.delete('toko/edit', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_delete_barang_not_found(self, client):
        token = create_token(True)
        data = {
            "barang_id":2
        }
        res = client.delete('toko/edit', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400