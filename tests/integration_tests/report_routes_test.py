from os import environ
environ['SQLALCHEMY_DATABASE_URI'] = environ.get("TEST_DATABASE_URI")


from models.models import OrderItem, Order, Product, Catalog, User
from common.config import setup_config
import json


class TestReport:
    @classmethod
    def setup_class(self):
        self.app = setup_config('test')
        from common.database import db_session

        self.user = User(username='trlababalan', password='$2b$12$q8ure0Zm6SZnD0I1uZGGiuaIEnDoDK85GUpIpdI5jHlJeyrEuNPy2')
        db_session.add(self.user)
        db_session.commit()
        
        self.catalog = Catalog(user_id=self.user.id)
        db_session.add(self.catalog)
        db_session.commit()

        self.user.catalog_id = self.catalog.id
        db_session.commit()

        self.product1 = Product(name="wiskey", price=10, quantity=1000, available=1000, image_url='http://slika.jpg', catalog_id=self.catalog.id)
        self.product2 = Product(name="beer", price=40, quantity=20, available=20, image_url='http://slika.jpg', catalog_id=self.catalog.id)
        db_session.add(self.product1)
        db_session.add(self.product2)
        db_session.commit()

        self.order1 = Order(address='some address', customer_name='some name')
        self.order2 = Order(address='some other address', customer_name='some other name')

        db_session.add(self.order1)
        db_session.add(self.order2)
        db_session.commit()

        self.order_item1 = OrderItem(product_id=self.product1.id, quantity=3, total=30, order_id=self.order1.id)
        self.order_item2 = OrderItem(product_id=self.product2.id, quantity=1, total=40, order_id=self.order2.id)
        db_session.add(self.order_item1)
        db_session.add(self.order_item2)
        db_session.commit()

        self.client = self.app.test_client()


    def test_highest_revenue_product(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_data().decode('utf-8')

        response = self.client.get('/api/report/highest-revenue-product', headers={'Authorization': f'Bearer {login_response}'}).get_json()
        product = response['product']

        assert product['id'] == self.product2.id


    def test_best_selling_product(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_data().decode('utf-8')

        response = self.client.get('/api/report/best-selling-product', headers={'Authorization': f'Bearer {login_response}'}).get_json()
        product = response['product']

        assert product['id'] == self.product1.id
