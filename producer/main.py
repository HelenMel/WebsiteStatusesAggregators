from checkers.website_checker import WebsiteChecker
from repositories.kafka import KafkaWriter
from utilities.json_serializer import JsonSerializer
from config.app_config import AppConfig
import schedule
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEBSITES = [
    "https://www.verkkokauppa.com/fi/catalog/59a/Lemmikit",
    "https://www.coursera.org/professional-certificates/google-it-support"
]

def main_job(checker, publisher):
    status = checker.check_get()
    if status is not None:
        publisher.send_sync(status)
        logger.info(f"send {status}")

def main_job_async(executor, checker, publisher):
    executor.submit(main_job, checker, publisher)

if __name__ == "__main__":
    app_config = AppConfig()
    checkers = [WebsiteChecker(url) for url in WEBSITES]
    publisher = KafkaWriter(app_config.kafka_config(), JsonSerializer.dataclass_to_json)
    run_sec = app_config.scheduler_config().request_status_every_sec
    executor = ThreadPoolExecutor(max_workers=2)

    for checker in checkers:
        schedule.every(run_sec).seconds.do(main_job_async, executor, checker, publisher)

    while True:
        try:
            schedule.run_pending()
        except KeyboardInterrupt as _:
            break
        except Exception as err:
            break
    executor.shutdown(wait=True)
    schedule.clear()
    publisher.close()