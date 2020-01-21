from blueprints import db
from flask_restful import fields


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(191), unique=True, nullable=False)
    username = db.Column(db.String(191), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    designer_status = db.Column(db.Boolean, default=False)

    response_fields = {
        'id': fields.Integer,
        'full_name': fields.String,
        'email': fields.String,
        'username': fields.String,
        'designer_status': fields.Boolean
    }

    jwt_claims_fields = {
        'id': fields.Integer,
        'full_name': fields.String,
        'email': fields.String,
        'username': fields.String,
        'designer_status': fields.Boolean
    }

    def __init__(self, full_name, email, username, password):
        self.full_name = full_name
        self.email = email
        self.username = username
        self.password = password
