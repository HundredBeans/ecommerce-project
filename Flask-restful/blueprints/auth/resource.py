import hashlib
import requests
import json
from flask import Blueprint
from flask_jwt_extended import create_access_token, get_jwt_claims, get_jwt_identity, jwt_required
from flask_restful import Api, Resource, marshal, reqparse
from ..auth.models import User
from blueprints import db, app
# password Encription
from password_strength import PasswordPolicy
# Gmail Function
import gmail
# Gmail message text
from message import register_html
# Lupa Password
from message import lupa_pass

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)


class RegisterUserResource(Resource):
    def post(self):
        policy = PasswordPolicy.from_names(
            length=6
        )

        parser = reqparse.RequestParser()
        parser.add_argument('full_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        validation = policy.test(args['password'])
        check_email = User.query.filter_by(email=args['email']).first()
        check_username = User.query.filter_by(
            username=args['username']).first()
        if check_email is not None:
            return {"status": "register gagal", "message": "email sudah terdaftar"}, 400, {"Content-type": "application/json"}
        if check_username is not None:
            return {"status": "register gagal", "message": "username sudah terpakai"}, 400, {"Content-type": "application/json"}
        if validation == []:
            hashed_pass = hashlib.md5(args['password'].encode()).hexdigest()
            user = User(args['full_name'], args['email'],
                        args['username'], hashed_pass)
            db.session.add(user)
            db.session.commit()
            app.logger.debug('DEBUG : %s', user)
            # Send Email using gmail API
            signature = gmail.get_signature()
            message = register_html.message.format(
                args['full_name']) + signature
            subject = "WELCOME {}, TO TEESIGNR!".format(args['full_name'])
            gmail.send_email("teesignr@gmail.com",
                             args["email"], subject, message)
            return {"status": "register berhasil", "user": marshal(user, User.response_fields)}, 200, {'Content-type': 'application/json'}
        else:
            return {"status": "register gagal", "message": "password tidak valid"}, 400, {"Content-type": "application/json"}

    def options(self):
        return {}, 200


class LoginUserResource(Resource):
    ### CREATE TOKEN ###
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        hashed_pass = hashlib.md5(args['password'].encode()).hexdigest()
        qry = User.query.filter_by(
            email=args['email']).filter_by(password=hashed_pass)
        userData = qry.first()
        if userData is not None:
            userData = marshal(userData, User.jwt_claims_fields)
            token = create_access_token(
                identity=userData['username'], user_claims=userData)
            return {'token': token}, 200, {'Content-Type': 'application/json'}
        else:
            return {'status': 'UNAUTHORIZED', 'message': 'Password atau Email salah'}, 401

    def options(self):
        return {}, 200


class ForgotPassResource(Resource):
     # FORGET PASSWORD
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json', required=True)
        args = parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()
        if user is not None:
            random_pass = lupa_pass.randomStringDigits(6)
            hashed_pass = hashlib.md5(random_pass.encode()).hexdigest()
            user.password = hashed_pass
            db.session.add(user)
            db.session.commit()
            signature = gmail.get_signature()
            message = lupa_pass.message.format(
                user.full_name, random_pass) + signature
            subject = "IMPORTANT! RESET PASSWORD FOR TEESIGNR"
            gmail.send_email("teesignr@gmail.com",
                             args["email"], subject, message)
            return {"status": "Password baru sudah terkirim ke email"}, 200, {'Content-Type': 'application/json'}
        else:
            return {"status": "Gagal", "message": "E-mail tidak terdaftar"}, 401

    def options(self):
        return {}, 200


api.add_resource(RegisterUserResource, '/register')
api.add_resource(LoginUserResource, '/login')
api.add_resource(ForgotPassResource, '/reset')
