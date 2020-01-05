import pytest, logging, json
from blueprints import app
from app import cache
from flask import request
from . import client, reset_db, create_token

class TestUserCrud():
    reset_db()
    def test_ganti_pass(self, client):
        token = create_token(True)
        data = {
            "old_password":"rahasia123",
            "new_password":"rahasia789"
        }
        res = client.patch('user/edit', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_ganti_pass_salah(self, client):
        token = create_token(True)
        data = {
            "old_password":"rahasia123",
            "new_password":"rahasia666"
        }
        res = client.patch('user/edit', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 401

    def test_ganti_pass_not_valid(self, client):
        token = create_token(True)
        data = {
            "old_password":"rahasia789",
            "new_password":"tes1"
        }
        res = client.patch('user/edit', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_get_info_user(self, client):
        token = create_token(False)
        res = client.get('user', headers={'Authorization' : 'Bearer ' + token})
        assert res.status_code == 200