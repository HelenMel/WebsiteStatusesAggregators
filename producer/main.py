from producer.checkers.websitechecker import WebsiteChecker
from producer.publishers.kafkatopicpublisher import KafkaTopicPublisher
from producer.publishers.jsonserializer import JsonSerializer
import schedule
import time

if __name__ == "__main__":
    topic = "WebsiteStatus"
    checker = WebsiteChecker("https://www.verkkokauppa.com/fi/myymalat/jatkasaari")
    publisher = KafkaTopicPublisher()
    publisher.connect(JsonSerializer.dataclass_to_json)
    def job():
        status = checker.check_get()
        if status is not None:
            publisher.send_sync(topic, status)
            print(status)

    schedule.every(3).seconds.do(job_func=job)
    while True:
        schedule.run_pending()
        time.sleep(1)