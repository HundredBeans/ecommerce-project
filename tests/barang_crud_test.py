import pytest, logging, json
from blueprints import app
from app import cache
from flask import request
from . import client, reset_db, create_token

class TestBarangCrud():
    reset_db()
    def test_list_barang_filter_terjual_desc(self, client):
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
        res = client.get('baju', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_list_barang_filter_terjual_asc(self, client):
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
        res = client.get('baju', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_list_barang_filter_harga_desc(self, client):
        token = create_token(True)
        data = {
            "p":1,
            "rp":20,
            "search":"",
            "harga minimal":100000,
            "harga maksimal":1000000,
            "jenis bahan":"Combed 30s",
            "orderby":"harga",
            "sort":"desc"
        }
        res = client.get('baju', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_list_barang_filter_harga_asc(self, client):
        token = create_token(True)
        data = {
            "p":1,
            "rp":20,
            "search":"",
            "harga minimal":100000,
            "harga maksimal":1000000,
            "jenis bahan":"Combed 30s",
            "orderby":"harga",
            "sort":"asc"
        }
        res = client.get('baju', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_list_barang_filter_id_desc(self, client):
        token = create_token(True)
        data = {
            "p":1,
            "rp":20,
            "search":"",
            "harga minimal":100000,
            "harga maksimal":1000000,
            "jenis bahan":"Combed 30s",
            "orderby":"id",
            "sort":"desc"
        }
        res = client.get('baju', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    def test_list_barang_filter_id_asc(self, client):
        token = create_token(True)
        data = {
            "p":1,
            "rp":20,
            "search":"",
            "harga minimal":100000,
            "harga maksimal":1000000,
            "jenis bahan":"Combed 30s",
            "orderby":"id",
            "sort":"asc"
        }
        res = client.get('baju', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_barang_id(self, client):
        res = client.get('baju/1')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_barang_id_notfound(self, client):
        res = client.get('baju/10')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_tambah_keranjang(self, client):
        token = create_token(False)
        data = {
            "jumlah":2,
            "ukuran":"XL"
        }
        res = client.put('baju/1', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_beli_barang(self, client):
        token = create_token(False)
        data = {
            "jumlah":2,
            "ukuran":"XL"
        }
        res = client.patch('baju/1', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200