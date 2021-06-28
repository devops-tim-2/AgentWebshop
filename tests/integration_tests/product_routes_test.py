from models.product import Product
from models.catalog import Catalog
from models.user import User
from common.config import setup_config
import pytest
import json


class TestProduct:
    @classmethod
    def setup_class(self):
        self.app, self.db = setup_config('test')

        self.user = User(username='trlababalan', password='$2b$12$q8ure0Zm6SZnD0I1uZGGiuaIEnDoDK85GUpIpdI5jHlJeyrEuNPy2')
        self.db.session.add(self.user)
        self.db.session.commit()
        
        self.catalog = Catalog(user_id=self.user.id)
        self.db.session.add(self.catalog)
        self.db.session.commit()

        self.user.catalog_id = self.catalog.id
        self.db.session.commit()

        self.product1 = Product(name="wiskey", price=10, quantity=1000, available=1000, image_url='http://slika.jpg', catalog_id=self.catalog.id)
        self.product2 = Product(name="beer", price=20, quantity=20, available=20, image_url='http://slika.jpg', catalog_id=self.catalog.id)
        self.db.session.add(self.product1)
        self.db.session.add(self.product2)
        self.db.session.commit()

        self.client = self.app.test_client()


    @classmethod
    def teardown_class(self):
        Product.query.filter_by(id=self.product1.id).delete()
        Product.query.filter_by(id=self.product2.id).delete()
        Catalog.query.filter_by(id=self.catalog.id).delete()
        User.query.filter_by(id=self.user.id).delete()
        
        self.db.session.commit()


    def test_get_all(self):
        response = self.client.get('/api/product').get_json()
        
        assert len(response['data']) == 2

    
    def test_get_happy(self):
        response = self.client.get(f'/api/product/{self.product1.id}').get_json()

        assert response['id'] == self.product1.id

    
    def test_get_sad(self):
        response = self.client.get(f'/api/product/{1000}')
        
        assert response.status_code == 500


    def test_create_happy(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_data().decode('utf-8')
        
        product_data = dict(name="vodka", price=20, quantity=20, image_url='http://slika.jpg')
        create_response = self.client.post('/api/product', data=json.dumps(product_data), headers={'Authorization': f'Bearer {login_response}', 'Content-Type': 'application/json'}).get_json()
        product_db = Product.query.get(create_response['id'])

        assert product_db.name == product_data['name']
        assert product_db.price == product_data['price']
        assert product_db.quantity == product_data['quantity']
        assert product_db.available == product_data['quantity']

    
    def test_create_sad(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_data().decode('utf-8')

        product_count_before = Product.query.count()
        product_data = dict(name="", price=20, quantity=20, image_url='http://slika.jpg')
        create_response = self.client.post('/api/product', data=json.dumps(product_data), headers={'Authorization': f'Bearer {login_response}', 'Content-Type': 'application/json'})
        product_count_after = Product.query.count()

        assert product_count_before == product_count_after


    def test_update_happy(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_data().decode('utf-8')

        product_data = dict(id=self.product1.id, name="vodka", price=20, quantity=20, image_url='http://slika.jpg')
        update_response = self.client.put('/api/product', data=json.dumps(product_data), headers={'Authorization': f'Bearer {login_response}', 'Content-Type': 'application/json'}).get_json()
        product_db = Product.query.get(self.product1.id)

        assert product_db.name == product_data['name']
        assert product_db.price == product_data['price']
        assert product_db.quantity == product_data['quantity']

    
    def test_update_sad(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_data().decode('utf-8')

        product_before = Product.query.get(self.product1.id).get_dict()
        product_data = dict(id=self.product1.id, name="", price=20, quantity=20, available=20, image_url='http://slika.jpg', catalog_id=self.catalog.id)
        update_response = self.client.put('/api/product', data=json.dumps(product_data), headers={'Authorization': f'Bearer {login_response}', 'Content-Type': 'application/json'})
        product_after = Product.query.get(self.product1.id).get_dict()

        assert product_before == product_after


    @pytest.mark.run(order=-2)
    def test_delete_happy(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_data().decode('utf-8')

        delete_response = self.client.delete(f'/api/product/{self.product1.id}', headers={'Authorization': f'Bearer {login_response}'})

        assert Product.query.get(self.product1.id) == None

    
    @pytest.mark.run(order=-1)
    def test_delete_sad(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_data().decode('utf-8')

        product_count_before = Product.query.count()
        delete_response = self.client.delete(f'/api/product/{self.product1.id}', headers={'Authorization': f'Bearer {login_response}'})
        product_count_after = Product.query.count()

        assert product_count_before == product_count_after
