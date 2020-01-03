import pytest, logging, json
from blueprints import app
from app import cache
from flask import request
from . import client, reset_db, create_token

class TestCheckoutCrud():
    reset_db()
    # Checkout barang dummy
    def test_beli_barang(self, client):
        token = create_token(False)
        data = {
            "jumlah":2,
            "ukuran":"XL"
        }
        res = client.patch('baju/1', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_list_barang_checkout(self, client):
        token = create_token(False)
        res = client.get('checkout', headers={'Authorization' : 'Bearer ' + token})
        assert res.status_code == 200

    def test_beli_barang_lagi(self, client):
        token = create_token(False)
        data = {
            "jumlah":2,
            "ukuran":"XL"
        }
        res = client.patch('baju/1', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_hapus_barang_checkout(self, client):
        token = create_token(False)
        res = client.delete('checkout', headers={'Authorization' : 'Bearer ' + token})
        assert res.status_code == 200