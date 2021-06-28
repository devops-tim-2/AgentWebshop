from models.order_item import OrderItem
from models.order import Order
from models.product import Product
from models.catalog import Catalog
from models.user import User
from common.config import setup_config
import json


class TestOrder:
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

        self.product = Product(name="wiskey", price=10, quantity=1000, available=1000, image_url='http://slika.jpg', catalog_id=self.catalog.id)
        self.db.session.add(self.product)
        self.db.session.commit()

        self.order1 = Order(address='some address', customer_name='some name')
        self.order2 = Order(address='some other address', customer_name='some other name')

        self.db.session.add(self.order1)
        self.db.session.add(self.order2)
        self.db.session.commit()

        self.order_item1 = OrderItem(product_id=self.product.id, quantity=1, total=10, order_id=self.order1.id)
        self.order_item2 = OrderItem(product_id=self.product.id, quantity=3, total=30, order_id=self.order2.id)
        self.db.session.add(self.order_item1)
        self.db.session.add(self.order_item2)
        self.db.session.commit()

        self.client = self.app.test_client()


    @classmethod
    def teardown_class(self):
        OrderItem.query.filter_by(id=self.order_item1.id).delete()
        OrderItem.query.filter_by(id=self.order_item2.id).delete()
        Order.query.filter_by(id=self.order1.id).delete()
        Order.query.filter_by(id=self.order2.id).delete()
        Product.query.filter_by(id=self.product.id).delete()
        Catalog.query.filter_by(id=self.catalog.id).delete()
        User.query.filter_by(id=self.user.id).delete()
        
        self.db.session.commit()


    def test_get_all(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_json()

        response = self.client.get('/api/order', headers={'Authorization': 'Bearer {}'.format(login_response)}).get_json()
        
        assert len(response) == 2

    
    def test_get_happy(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_json()

        response = self.client.get('/api/order/{}'.format(self.order1.id), headers={'Authorization': 'Bearer {}'.format(login_response)}).get_json()

        assert response['id'] == self.order1.id

    
    def test_get_sad(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_json()

        response = self.client.get('/api/order/{}'.format(1000), headers={'Authorization': 'Bearer {}'.format(login_response)})
        
        assert response.status_code == 404


    def test_create_happy(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_json()
        
        order_data = dict(order_items=[dict(product_id=self.product.id, quantity=1)], address='some address', customer_name='some name')
        create_response = self.client.post('/api/order', data=json.dumps(order_data), headers={'Authorization': 'Bearer {}'.format(login_response), 'Content-Type': 'application/json'}).get_json()
        order_db = Order.query.get(create_response['id'])

        assert len(order_db.order_items) == len(order_data['order_items'])
        assert order_db.address == order_data['address']
        assert order_db.customer_name == order_data['customer_name']

    
    def test_create_sad(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_json()

        order_count_before = Product.query.count()
        order_data = dict(order_items=[json.dumps(dict(product_id=self.product.id, quantity=1001))], address='some address', customer_name='some name')
        create_response = self.client.post('/api/order', data=json.dumps(order_data), headers={'Authorization': 'Bearer {}'.format(login_response), 'Content-Type': 'application/json'}).get_json()
        order_count_after = Product.query.count()

        assert order_count_before == order_count_after
