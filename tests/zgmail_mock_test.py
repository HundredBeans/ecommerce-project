import pytest, logging, json
from blueprints import app
from app import cache
from flask import request
from . import client, reset_db, create_token
from unittest import mock
from unittest.mock import patch
import gmail

# DIKASIH NAMA zgmail_mock_test biar testnya dijalanin paling terakhir, soalnya ada register toko yang 
# nantinya bisa ngerusak test yang lain
class TestGmailMock():
    reset_db()
    def mocked_send_email(sender, to, subject, message):
        print('send email successfully mocked')

    def mocked_get_signature():
        print('get signature successfully mocked')
        return "signature"


    # Mock test
    @mock.patch.object(gmail, "send_email", side_effect=mocked_send_email)
    @mock.patch.object(gmail, "get_signature", side_effect=mocked_get_signature)
    def test_register(self, test_get_signature_mock, test_send_email_mock, client):
        data = {
            "full_name":"Achmad Rafiq",
            "email":"minangjawara@gmail.com",
            "username":"ArtisThailand",
            "password":"rahasia123"
        }
        res = client.post('auth/register', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200

    @mock.patch.object(gmail, "send_email", side_effect=mocked_send_email)
    @mock.patch.object(gmail, "get_signature", side_effect=mocked_get_signature)
    def test_forget_pass(self, test_get_signature_mock, test_send_email_mock, client):
        data = {
            "email":"youdontsayhuman@gmail.com"
        }
        res = client.get('auth/reset', json=data)
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Jual barang dummy biar nantinya bisa test beli barang, id barang = 3
    def test_jual_barang3(self, client):
        token = create_token(True)
        data = {
            "nama_barang":"KAOS LENGAN PENDEK THE POPO -THE BEATLES WHITE-",
            "keuntungan":15000,
            "desain":"https://cf.shopee.co.id/file/71a6b24e95b35a915bb3cdcfe3cfc309_tn",
            "jenis_bahan":"Combed 30s",
            "deskripsi":"Material: Cotton Combed 30s. Produk Warna: Putih"
        }
        res = client.post('toko/jual', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # beli barang 3 hasil jual sebelumnya
    def test_beli_barang3(self, client):
        token = create_token(False)
        data = {
            "jumlah":2,
            "ukuran":"XL"
        }
        res = client.patch('baju/3', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # beli barang 2 hasil jual dari test sebelumnya
    def test_beli_barang2(self, client):
        token = create_token(False)
        data = {
            "jumlah":1,
            "ukuran":"XL"
        }
        res = client.patch('baju/2', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    @mock.patch.object(gmail, "send_email", side_effect=mocked_send_email)
    @mock.patch.object(gmail, "get_signature", side_effect=mocked_get_signature)
    def test_checkout_belanja(self, test_get_signature_mock, test_send_email_mock, client):
        token = create_token(False)
        data = {
            "nama_penerima":"Mohammad Daffa",
            "no_telepon":"08159898344",
            "alamat_penerima":"JL.Tidar No.23, Kecamatan Galunggung, Kota Malang, Provinsi Jawa Timur",
            "metode_pembayaran":"CASH ON DELIVERY"
        }
        res = client.post('checkout', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    @mock.patch.object(gmail, "send_email", side_effect=mocked_send_email)
    @mock.patch.object(gmail, "get_signature", side_effect=mocked_get_signature)
    def test_register_toko(self, test_get_signature_mock, test_send_email_mock, client):
        token = create_token(False)
        data = {
            "nama_toko":"T-Shirt Artis Thailand",
	        "deskripsi":"T-Shirt UwU by Achmad Rafiq"
        }
        res = client.post('toko/register', json=data, headers={'Authorization' : 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Get info user
    def test_get_info_user(self, client):
        token = create_token(True)
        res = client.get('user', headers={'Authorization' : 'Bearer ' + token})
        assert res.status_code == 200

    def test_get_info_user_buyer(self, client):
        token = create_token(False)
        res = client.get('user', headers={'Authorization' : 'Bearer ' + token})
        assert res.status_code == 200