from dataclasses import dataclass
from typing import Optional

@dataclass
class WebsiteStatus():
    """Class for keeping information about status. Time specified in
    milliseconds
    """
    uuid: str
    url: str
    occured_at: int
    response_time: Optional[int]
    error_code: Optional[int]