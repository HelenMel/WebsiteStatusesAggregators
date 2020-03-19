from producer.dto.websitestatus import WebsiteStatus
import logging
import requests
from requests.exceptions import HTTPError
from typing import Optional

logger = logging.getLogger(__name__)

class WebsiteChecker():
    """This class is responsible for checking statuses for particular website

    Args:
        url (str): website url
    """
    def __init__(self, url):
        self.url = url

    def check_get(self) -> Optional[str]:
        error_code = None
        res_time_sec = None
        try:
            response = requests.get(self.url)
            res_time_sec = response.elapsed.total_seconds()
            # TODO: add content checking
            response.raise_for_status()
        except HTTPError as http_error:
            error_code = http_error.response.status_code
        except Exception as err:
            logging.error("Unexpected error during status check for %s" % self.url, err)
            return None
        finally:
            return WebsiteStatus(self.url, res_time_sec, error_code)