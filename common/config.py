from os import environ
from typing import Tuple
from flask_cors import CORS
from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.report_routes import report_api
from common.database import db
from models.product import Product
from models.order import Order
from models.order_item import OrderItem
from models.user import User
from models.catalog import Catalog


DevConfig = {
    'DEBUG': True,
    'DEVELOPMENT': True,
    'SQLALCHEMY_DATABASE_URI': f'{environ.get("DB_TYPE")}+{environ.get("DB_DRIVER")}://{environ.get("DB_USER")}:{environ.get("DB_PASSWORD")}@{environ.get("DB_HOST")}/{environ.get("DB_NAME")}',
    'SQLALCHEMY_ECHO': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
}


TestConfig = {
    'DEBUG': False,
    'DEVELOPMENT': True,
    'SQLALCHEMY_DATABASE_URI': f'{environ.get("TEST_DATABASE_URI")}',
    'SQLALCHEMY_ECHO': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
}


config: dict = {
    'dev': DevConfig,
    'test': TestConfig
}


def setup_config(cfg_name: str) -> Tuple[Flask, SQLAlchemy]:
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(report_api, url_prefix='/api/report')

    cfg = config.get(cfg_name)
    for key in cfg.keys():
        app.config[key] = cfg[key]

    app.app_context().push()
    db.init_app(app)

    with app.app_context():
        db.create_all()

    if cfg_name == 'test':
        OrderItem.query.delete()
        Order.query.delete()
        Product.query.delete()
        Catalog.query.delete()
        User.query.delete()

    return app, db
