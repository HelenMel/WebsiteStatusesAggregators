from dataclasses import dataclass
from typing import Optional

@dataclass
class WebsiteStatus:
    '''Class for keeping information about status'''
    url: str
    response_time: float
    error_code: Optional[int]