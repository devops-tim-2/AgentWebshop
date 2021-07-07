from os import environ
from flask_cors import CORS
from flask.app import Flask
from flask_wtf import CSRFProtect


config = {
    'test': 'TEST_DATABASE_URI',
    'dev': 'DEV_DATABASE_URI'
}



def setup_config(cfg_name: str):
    environ['SQLALCHEMY_DATABASE_URI'] = environ.get(config[cfg_name])
    
    app = Flask(__name__, static_url_path='')
    if environ.get('ENABLE_CSRF') == 1:
        app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
        app.config['WTF_CSRF_SECRET_KEY'] = environ.get('WTF_CSRF_SECRET_KEY')
        csrf = CSRFProtect()
        csrf.init_app(app)
        
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "send_wildcard": "False"}})

    from common.database import init_db
    init_db()

    from routes.product_routes import product_api
    from routes.order_routes import order_api
    from routes.report_routes import report_api
    from routes.user_routes import user_api
    from routes.catalog_routes import catalog_api
    app.register_blueprint(product_api, url_prefix='/api/product')
    app.register_blueprint(order_api, url_prefix='/api/order')
    app.register_blueprint(report_api, url_prefix='/api/report')
    app.register_blueprint(catalog_api, url_prefix='/api/catalog')
    app.register_blueprint(user_api, url_prefix="/api")


    from models.models import Product, Order, OrderItem, User, Catalog
    if cfg_name == 'test':
        OrderItem.query.delete()
        Order.query.delete()
        Product.query.delete()
        Catalog.query.delete()
        User.query.delete()

    return app
