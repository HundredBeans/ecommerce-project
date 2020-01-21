import json, os
from datetime import datetime, timedelta
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_claims, verify_jwt_in_request
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Resource, reqparse
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
CORS(app)

app.config['APP_DEBUG'] = True

### JWT ###
app.config['JWT_SECRET_KEY'] = 'SFsieaaBsLEpecP675r243faM8oSB2hV'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

### SQL ALCHEMY CONFIG ###
try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:kacang100@project-ecommerce.cbzk7tczg77b.ap-southeast-1.rds.amazonaws.com:3306/project-ecommerce-test'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:kacang100@project-ecommerce.cbzk7tczg77b.ap-southeast-1.rds.amazonaws.com:3306/projectecommerce'
except Exception as e:
    raise e

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

### AFTER REQUEST ###
@app.after_request
def after_request(response):
    try:
        request0 = request.get_json()
    except:
        request0 = request.args.to_dict()
    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s", json.dumps({
            'status_code': response.status_code,
            'method': request.method,
            'code': response.status,
            'uri': request.full_path,
            'request': request0,
            'response': json.loads(response.data.decode('utf-8'))
        }))
    else:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps({
            'status_code': response.status_code,
            'method': request.method,
            'code': response.status,
            'uri': request.full_path,
            'request': request0,
            'response': json.loads(response.data.decode('utf-8'))
        }))
    return response

### IMPORT BLUEPRINTS ###
from blueprints.auth.resource import bp_auth
from blueprints.toko.resource import bp_toko
from blueprints.barang.resource import bp_barang
from blueprints.keranjang.resource import bp_keranjang
from blueprints.checkout.resource import bp_checkout
from blueprints.user.resource import bp_user

app.register_blueprint(bp_auth, url_prefix='/auth')
app.register_blueprint(bp_toko, url_prefix='/toko')
app.register_blueprint(bp_barang, url_prefix='/baju')
app.register_blueprint(bp_keranjang, url_prefix='/keranjang')
app.register_blueprint(bp_checkout, url_prefix='/checkout')
app.register_blueprint(bp_user, url_prefix='/user')

db.create_all()
