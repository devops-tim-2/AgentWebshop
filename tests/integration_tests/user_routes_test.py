from os import environ
environ['SQLALCHEMY_DATABASE_URI'] = environ.get("TEST_DATABASE_URI")

from flask import Flask
from models.models import OrderItem, Order, Product, Catalog, User
from common.config import setup_config
import json


class TestUser:
    @classmethod
    def setup_class(self):
        self.app = setup_config('test')
        from common.database import db_session

        self.user = User(username='trlababalan', password='$2b$12$q8ure0Zm6SZnD0I1uZGGiuaIEnDoDK85GUpIpdI5jHlJeyrEuNPy2')
        db_session.add(self.user)
        db_session.commit()

        self.client = self.app.test_client()


    def test_login_happy(self):
        data = dict(username=self.user.username, password='admin')
        response = self.client.post('/auth', data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == 200

    
    def test_login_sad(self):
        data = dict(username='admin2', password='admin')
        response = self.client.post('/auth', data=json.dumps(data), content_type='application/json')
        
        assert response.status_code == 404
