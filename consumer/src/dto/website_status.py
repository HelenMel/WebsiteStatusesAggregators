from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class WebsiteStatus():
    '''Class for keeping information about status. Time specified in milliseconds'''
    id: str
    url: str
    occured_at: int
    response_time: Optional[int]
    error_code: Optional[int]

    @classmethod
    def from_dict(cls, d: dict):
        try:
            new_item = cls(d['id'],
                           d['url'],
                           d['occured_at'],
                           d.get('response_time', None),
                           d.get('error_code', None))
            return new_item
        except KeyError as key_err:
            logger.error(f'Parsing error. Required field is missing {str(key_err)}')
            return None

