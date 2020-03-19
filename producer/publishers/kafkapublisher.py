from kafka import KafkaProducer

class KafkaPublisher():

    def connect(self):
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'])