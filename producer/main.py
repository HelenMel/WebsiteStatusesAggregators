from producer.checkers.website_checker import WebsiteChecker
from producer.repositories.kafka import KafkaWriter
from producer.utilities.json_serializer import JsonSerializer
from producer.config.app_config import AppConfig
import schedule
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEBSITES = [
    "https://www.verkkokauppa.com/fi/catalog/59a/Lemmikit",
    "https://www.coursera.org/professional-certificates/google-it-support"
]

class WebsiteStatusProducer():
    """This class accept list of websites as a parameter,
        check websites statuses and store statuses to kafka

        :param websites: list of websites to query
        :param request_every: request frequency in seconds
    """
    def __init__(self, websites = WEBSITES, request_every = 5):
        self.websites = websites
        self.request_every = request_every
        self.is_running = False
        self._publisher = None
        self._app_config = None

    @property
    def app_config(self):
        if self._app_config is None:
            self._app_config = AppConfig()
        return self._app_config

    @property
    def publisher(self):
        if self._publisher is None:
            self._publisher = KafkaWriter(self.app_config.kafka_config(), JsonSerializer.dataclass_to_json)
        return self._publisher

    def run(self):
        checkers = [WebsiteChecker(url) for url in self.websites]
        executor = ThreadPoolExecutor(max_workers=2)
        self.is_running = True

        for checker in checkers:
            schedule.every(self.request_every).seconds.do(self._main_job_async, executor, checker, self.publisher)

        while self.is_running:
            try:
                schedule.run_pending()
            except KeyboardInterrupt as _:
                break
            except Exception as err:
                logger.error(f"Job will be finished because of an error: {err}")
                break
        executor.shutdown(wait=True)
        schedule.clear()
        publisher.close()

    def _main_job(self, checker, publisher):
        status = checker.check_get()
        if status is not None:
            publisher.send_sync(status)
            logger.info(f"send {status}")

    def _main_job_async(self, executor, checker, publisher):
        executor.submit(self._main_job, checker, publisher)

if __name__ == "__main__":
    producer = WebsiteStatusProducer()
    producer.run()