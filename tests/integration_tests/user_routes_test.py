from flask import Flask
from models.user import User
from common.config import setup_config
import json


class TestUser:
    @classmethod
    def setup_class(self):
        self.app, self.db = setup_config('test')

        self.user = User(username='trlababalan', password='$2b$12$q8ure0Zm6SZnD0I1uZGGiuaIEnDoDK85GUpIpdI5jHlJeyrEuNPy2')
        self.db.session.add(self.user)
        self.db.session.commit()

        self.client = self.app.test_client()


    @classmethod
    def teardown_class(self):
        User.query.filter_by(id=self.user.id).delete()
        
        self.db.session.commit()


    def test_login_happy(self):
        data = dict(username=self.user.username, password='admin')
        response = self.client.post('/auth', data=json.dumps(data), content_type='application/json').get_json()
        
        assert response['code'] == 200

    
    def test_login_sad(self):
        data = dict(username='admin2', password='admin')
        response = self.client.post('/auth', data=json.dumps(data), content_type='application/json').get_json()
        
        assert response['code'] == 404
