import json
from common.database import db_session
from models.models import User, Catalog


class UserConsumer:
    def __init__(self, channel):
        self.exchange_name = 'user'
        self.channel = channel
        channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')
        q = channel.queue_declare(queue='')
        channel.queue_bind(exchange=self.exchange_name, queue=q.method.queue)
        channel.basic_consume(queue=q.method.queue, on_message_callback=self.on_message, auto_ack=True)

    def on_message(self, ch, method, properties, body):
        try:
            data = json.loads(body)
            if properties.content_type == 'agent.request.created':            
                user = User(id=data['id'], username=data['username'], password=data['password'])
                db_session.add(user)
                db_session.commit()
                catalog = Catalog(user_id=data['id'])
                db_session.add(catalog)
                db_session.commit()
                user.catalog_id = catalog.id
                db_session.commit()
        except Exception:
            # don't crash
            pass