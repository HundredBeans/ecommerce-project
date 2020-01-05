import pytest, logging, json
from blueprints import app
from app import cache
from flask import request
from . import client, reset_db, create_token

class TestKeranjangCrud():
    reset_db()
    # Tambah keranjang dummy
    def test_tambah_keranjang(self, client):
        token = create_token(False)
        data = {
            "jumlah":2,
            "ukuran":"XL"
        }
        res = client.put('baju/1', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_list_keranjang_sort_harga_desc(self, client):
        token = create_token(False)
        data = {
            "p":1,
            "rp":20,
            "search":"",
            "orderby":"harga",
            "sort":"desc"
        }
        res = client.get('keranjang', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_list_keranjang_sort_harga_asc(self, client):
        token = create_token(False)
        data = {
            "p":1,
            "rp":20,
            "search":"",
            "orderby":"harga",
            "sort":"asc"
        }
        res = client.get('keranjang', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_list_keranjang_sort_id_desc(self, client):
        token = create_token(False)
        data = {
            "p":1,
            "rp":20,
            "search":"",
            "orderby":"id",
            "sort":"desc"
        }
        res = client.get('keranjang', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_list_keranjang_sort_id_asc(self, client):
        token = create_token(False)
        data = {
            "p":1,
            "rp":20,
            "search":"",
            "orderby":"id",
            "sort":"asc"
        }
        res = client.get('keranjang', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_edit_keranjang(self, client):
        token = create_token(False)
        data = {
            "id":2,
            "jumlah":1,
            "ukuran":"L"
        }
        res = client.put('keranjang', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_edit_keranjang_gagal(self, client):
        token = create_token(False)
        data = {
            "id":1,
            "jumlah":1,
            "ukuran":"L"
        }
        res = client.put('keranjang', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_checkout_keranjang(self, client):
        token = create_token(False)
        data = {
            "id":[2]
        }
        res = client.patch('keranjang', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_checkout_keranjang_fail(self, client):
        token = create_token(False)
        data = {
            "id":[2]
        }
        res = client.patch('keranjang', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 403

    def test_hapus_semua_keranjang(self, client):
        token = create_token(False)
        res = client.delete('keranjang', headers={'Authorization' : 'Bearer ' + token})
        assert res.status_code == 200

    def test_hapus_spesifik_keranjang(self, client):
        token = create_token(True)
        data = {
            "id":[1]
        }
        res = client.delete('keranjang', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200