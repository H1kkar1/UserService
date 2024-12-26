import json

from pika import PlainCredentials, ConnectionParameters, BlockingConnection

from app.config import settings


def confirm_handler(method_frame) -> str:
    if method_frame.method.NAME == 'Basic.Ack':
        return "Сообщение успешно доставлено в очередь"
    elif method_frame.method.NAME == 'Basic.Nack':
        return "Сообщение не было доставлено в очередь"


class BrokerHelper:
    def __init__(
            self,
            host: str,
            port: int,
            credentials: PlainCredentials,
    ) -> None:
        self.rmq_parameters = ConnectionParameters(
            host=host,
            port=port,
            credentials=credentials
        )
        with BlockingConnection(self.rmq_parameters) as connection:
            with connection.channel() as channel:
                channel.queue_declare("profile_image")
        # self.rmq_channel.queue_declare("manga_classic")

    def user_profile_photo_operation(self, operation: str, photo_name: str, photo_type: str, photo_data: bytes):
        with BlockingConnection(self.rmq_parameters) as connection:
            with connection.channel() as channel:
                message = json.dumps({
                        'operation': operation,
                        'photo_name': photo_name,
                        'photo_type': photo_type,
                        'photo_data': photo_data.hex(),
                    })
                channel.basic_publish(
                    exchange='',
                    routing_key="profile_image",
                    body=message)
                result = channel.add_on_return_callback(confirm_handler)
                return result

    def user_profile_photo_update(self, operation: str, photo_name: str, photo_type: str, photo_data: bytes):
        with BlockingConnection(self.rmq_parameters) as connection:
            with connection.channel() as channel:
                message = json.dumps({
                        'operation': operation,
                        'photo_name': photo_name,
                        'photo_type': photo_type,
                        'photo_data': photo_data.hex(),
                    })
                channel.basic_publish(
                    exchange='',
                    routing_key="profile_image",
                    body=message)
                result = channel.add_on_return_callback(confirm_handler)
                return result

    def user_profile_photo_delete(self, operation: str, photo_name: str):
        with BlockingConnection(self.rmq_parameters) as connection:
            with connection.channel() as channel:
                message = json.dumps({
                        'operation': operation,
                        'photo_name': photo_name,
                    })
                channel.basic_publish(
                    exchange='',
                    routing_key="profile_image",
                    body=message)
                result = channel.add_on_return_callback(confirm_handler)
                return result



rmq = BrokerHelper(
    host=settings.rmq.host,
    port=settings.rmq.port,
    credentials=PlainCredentials(
        username=settings.rmq.username,
        password=settings.rmq.password,
    ),
)
