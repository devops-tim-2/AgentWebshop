from models.order_item import OrderItem
from models.order import Order
from models.product import Product
from models.catalog import Catalog
from models.user import User
from common.config import setup_config
import json


class TestReport:
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
        self.product2 = Product(name="beer", price=40, quantity=20, available=20, image_url='http://slika.jpg', catalog_id=self.catalog.id)
        self.db.session.add(self.product1)
        self.db.session.add(self.product2)
        self.db.session.commit()

        self.order1 = Order(address='some address', customer_name='some name')
        self.order2 = Order(address='some other address', customer_name='some other name')

        self.db.session.add(self.order1)
        self.db.session.add(self.order2)
        self.db.session.commit()

        self.order_item1 = OrderItem(product_id=self.product1.id, quantity=3, total=30, order_id=self.order1.id)
        self.order_item2 = OrderItem(product_id=self.product2.id, quantity=1, total=40, order_id=self.order2.id)
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
        Product.query.filter_by(id=self.product1.id).delete()
        Product.query.filter_by(id=self.product2.id).delete()
        Catalog.query.filter_by(id=self.catalog.id).delete()
        User.query.filter_by(id=self.user.id).delete()
        
        self.db.session.commit()


    def test_highest_revenue_product(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_data()

        response = self.client.get('/api/report/highest-revenue-product', headers={'Authorization': 'Bearer {}'.format(login_response)}).get_json()
        product = response['product']

        assert product['id'] == 2


    def test_best_selling_product(self):
        login_data = dict(username=self.user.username, password='admin')
        login_response = self.client.post('/auth', data=json.dumps(login_data), content_type='application/json').get_data()

        response = self.client.get('/api/report/best-selling-product', headers={'Authorization': 'Bearer {}'.format(login_response)}).get_json()
        product = response['product']

        assert product['id'] == 1
