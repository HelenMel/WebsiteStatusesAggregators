from dto.website_status import WebsiteStatus
import logging
import requests
from requests.exceptions import HTTPError
from typing import Optional
import time
import uuid

logger = logging.getLogger(__name__)

class WebsiteChecker():
    """This class is responsible for checking statuses for particular website

    Args:
        url (str): website url
    """
    def __init__(self, url):
        self.url = url

    def check_get(self) -> Optional[WebsiteStatus]:
        error_code = None
        event_id = str(uuid.uuid4())
        current_time_milli = int(round(time.time() * 1000))
        response_time = None
        try:
            response = requests.get(self.url)
            response_time = int(response.elapsed.total_seconds() * 1000)
            # TODO: add content checking with regex
            response.raise_for_status()
        except HTTPError as http_error:
            error_code = http_error.response.status_code
        except Exception as err:
            logging.error(f"Unexpected error during status check for {self.url} error: {err}")
            return None
        finally:
            return WebsiteStatus(event_id, self.url, current_time_milli, response_time, error_code)