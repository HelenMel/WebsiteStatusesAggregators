from checkers.website_checker import WebsiteChecker
from repositories.kafka import KafkaWriter
from utilities.json_serializer import JsonSerializer
import schedule

if __name__ == "__main__":
    topic = "WebsiteStatus"
    checker = WebsiteChecker("https://www.verkkokauppa.com/fi/myymalat/jatkasaari")
    publisher = KafkaWriter()
    publisher.connect(JsonSerializer.dataclass_to_json)
    def job():
        status = checker.check_get()
        if status is not None:
            publisher.send_sync(topic, status)
            print(status)

    schedule.every(5).seconds.do(job_func=job)
    while True:
        try:
            schedule.run_pending()
        except KeyboardInterrupt as _:
            break
        except Exception as err:
            break
    schedule.clear()
    publisher.close()