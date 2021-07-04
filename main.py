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

@app.route('/static/<path:path>')
def send(path):
    return send_from_directory('../public', path)


if __name__ == '__main__':
    app.run(host=environ.get('FLASK_RUN_HOST'))
