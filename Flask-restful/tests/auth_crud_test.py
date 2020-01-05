import pytest, logging, json
from blueprints import app
from app import cache
from flask import request
from . import client, reset_db, create_token

class TestAuthCrud():
    reset_db()
    # register gagal
    def test_register_fail_email(self, client):
        data = {
            "full_name":"Dobleh Jamal",
            "email":"daffa@alterra.id",
            "username":"Fadafuq",
            "password":"test"
        }
        res = client.post('/auth/register', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 400

    # register gagal
    def test_register_fail_username(self, client):
        data = {
            "full_name":"Dobleh Jamal",
            "email":"daffa@alterra.com",
            "username":"Fadafuq",
            "password":"test"
        }
        res = client.post('/auth/register', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 400

    # register gagal
    def test_register_fail_password(self, client):
        data = {
            "full_name":"Dobleh Jamal",
            "email":"daffa@alterra.com",
            "username":"Fadafuq1",
            "password":"test"
        }
        res = client.post('/auth/register', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_login_user(self, client):
        create_token()

    def test_login_user_fail(self, client):
        data = {
            "email":"auahgelap@gmail.com",
            "password":"rahasia123"
        }
        res = client.post('auth/login', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 401

    def test_reset_pass_fail(self, client):
        data = {
            "email":"auahgelap@gmail.com"
        }
        res = client.get('auth/reset', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 401