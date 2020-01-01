import hashlib
from flask import Blueprint
from flask_jwt_extended import create_access_token, get_jwt_claims, get_jwt_identity, jwt_required
from flask_restful import Api, Resource, marshal, reqparse
from ..auth.models import User
from blueprints import db, app
#password Encription
from password_strength import PasswordPolicy

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class RegisterUserResource(Resource):
    def post(self):
        policy = PasswordPolicy.from_names(
            length = 6,
            numbers = 1
        )

        parser = reqparse.RequestParser()
        parser.add_argument('full_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        validation = policy.test(args['password'])
        if validation == []:
            hashed_pass = hashlib.md5(args['password'].encode()).hexdigest()
            user = User(args['full_name'], args['email'], args['username'], hashed_pass)
            db.session.add(user)
            db.session.commit()
            app.logger.debug('DEBUG : %s', user)
            return {"status":"register berhasil", "user":marshal(user, User.response_fields)}, 200, {'Content-type': 'application/json'}
        else:
            return {"status":"register gagal", "message":"password tidak valid"}, 400, {"Content-type":"application/json"}

class LoginUserResource(Resource):
    ### CREATE TOKEN ###
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        hashed_pass = hashlib.md5(args['password'].encode()).hexdigest()
        qry = User.query.filter_by(email=args['email']).filter_by(password=hashed_pass)
        userData = qry.first()
        if userData is not None:
            userData = marshal(userData, User.jwt_claims_fields)
            token = create_access_token(identity=userData['username'], user_claims=userData)
            return {'token': token}, 200, {'Content-Type': 'application/json'}
        else:
            return {'status': 'UNAUTHORIZED', 'message':'Password atau Email salah'}, 401, 
            {'Content-Type': 'application/json'}

api.add_resource(RegisterUserResource, '/register')
api.add_resource(LoginUserResource, '/login')
