'''
Core module.
'''

import requests
from typing import Literal

from . import utils
from . import consts
from .objects import Video, Query

class Core:
    '''
    Represents a core.
    '''
    
    def __init__(self, session: requests.Session = None) -> None:
        '''
        Initialise a new core instance.
        
        Args:
            session (requests.Session): Session to send requests with.
        '''
        
        # Initialise session
        self.session = session or requests.Session()
        self.session.cookies.set('in_d4', '1')
    
    def call(self,
             func: str,
             method: str = 'GET',
             data: dict = None,
             headers: dict = {},
             timeout: int = 30,
             throw: bool = True) -> requests.Response:
        '''
        Send a custom request to the target servers.
        
        Args:
            func (str): URL or root function to call.
            data (dict): Request payload.
            headers (dict): additional headers to send.
            timeout (int): maximum request timeout.
            throw (bool): Wether to err if the request fails.
        
        Returns:
            requests.Response: The returned response.
        '''
        
        if not func.startswith('http'):
            func = utils.concat(consts.ROOT, func)
        
        response = self.session.request(
            method = method,
            url = func,
            data = data,
            timeout = timeout,
            headers = consts.HEADERS | headers
        )
        
        if throw:
            response.raise_for_status()
        
        return response
    
    def get(self, video: str) -> Video:
        '''
        Fetch a video.
        
        Args:
            video (str): Video URL or slug.
        '''
        
        if video.startswith('http'):
            url = video
        
        elif not '/' in video:
            url = utils.concat(consts.HOST, 'videos/hentai', video)
        
        else:
            raise ValueError(f'Invalid to resolve video URL: {video}')
        
        return Video(self, url)

    def search(self,
               query: str,
               tags: consts.search_tags | list[consts.search_tags] = [],
               tags_mode: Literal['AND', 'OR'] = 'AND',
               brands: consts.search_brands | list[consts.search_brands] = [],
               blacklist: consts.search_tags | list[consts.search_tags] = [],
               order: consts.search_orders = 'created_at_unix',
               ordering: Literal['+', '-'] = '+',
               ) -> Query:
        '''
        Open a new search query.
        '''
        
        payload = {
            'search_text': query,
            'tags': tags,
            'tags_mode': tags_mode,
            'brands': brands,
            'blacklist': blacklist,
            'order_by': order,
            'ordering': ('asc', 'desc')[ordering == '+']
        }
        
        return Query(payload)

# EOF