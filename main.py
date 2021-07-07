from os import environ
from common.config import setup_config
from flask import send_from_directory
import os
app = setup_config('dev')

@app.route('/')
def send_index():
    return send_from_directory('../public/components/index/', 'index.html')

@app.route('/login')
def send_login():
    return send_from_directory('../public/components/login/', 'login.html')

@app.route('/shop')
def send_shop():
    return send_from_directory('../public/components/shop/', 'shop.html')

@app.route('/product')
def send_product():
    return send_from_directory('../public/components/product/', 'product.html')

@app.route('/order')
def send_order():
    return send_from_directory('../public/components/order/', 'order.html')


@app.route('/manage')
def send_manage():
    return send_from_directory('../public/components/manage/', 'manage.html')


@app.route('/notfound')
def send_notfound():
    return send_from_directory('../public/components/notfound/', 'notfound.html')

@app.route('/static/<path:path>')
def send(path):
    return send_from_directory('../public', path)


if __name__ == '__main__':
    app.run(host=environ.get('FLASK_RUN_HOST'))
