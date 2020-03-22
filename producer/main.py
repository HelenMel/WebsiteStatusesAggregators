from checkers.website_checker import WebsiteChecker
from repositories.kafka import KafkaWriter
from utilities.json_serializer import JsonSerializer
from config.app_config import AppConfig
import schedule

WEBSITES = [
    "https://www.verkkokauppa.com/fi/catalog/59a/Lemmikit",
    "https://www.coursera.org/professional-certificates/google-it-support"
]

def main_job(checker, publisher):
    status = checker.check_get()
    if status is not None:
        publisher.send_sync(status)
        print(f"done {status}")

if __name__ == "__main__":
    app_config = AppConfig()
    checker = WebsiteChecker(WEBSITES[0])
    publisher = KafkaWriter(app_config.kafka_config(), JsonSerializer.dataclass_to_json)
    run_sec = app_config.scheduler_config().request_status_every_sec

    schedule.every(run_sec).seconds.do(main_job, checker, publisher)
    while True:
        try:
            schedule.run_pending()
        except KeyboardInterrupt as _:
            break
        except Exception as err:
            break
    schedule.clear()
    publisher.close()