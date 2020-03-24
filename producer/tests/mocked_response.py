from requests.exceptions import HTTPError
from datetime import timedelta

class MockedResponse:
    def __init__(self, seconds, status_code, error = False):
        self.elapsed = timedelta(seconds=seconds)
        self.seconds = seconds
        self.status_code = status_code
        self.error = error

    def raise_for_status(self):
        if self.error:
            raise HTTPError(response=MockedResponse(self.seconds, self.status_code))