from __future__ import annotations

import json
from functools import cache
from typing import TYPE_CHECKING, Generator

from . import Video
from .. import utils
from .. import consts

if TYPE_CHECKING:
    from .. import Core

class Query:
    '''
    Represents a query iterator.
    '''
    
    def __init__(self, core: Core, payload: dict) -> None:
        '''
        Open a new query.
        '''
        
        self.core = core
        self.payload = payload
    
    @cache
    def __len__(self) -> int:
        
        payload = self.payload | {'page': 1}
        raw = self.core.call(consts.SEARCH_API, 'POST', payload)
        return raw.json()['nbHits']
    
    def __getitem__(self, index: int | slice) -> Video | Generator[Video, None, None]:
        '''
        Get one or multiple items from the query.
        '''
        
        assert isinstance(index, (int, slice))
        
        if isinstance(index, int):
            return self.get(index)

        def wrap() -> Generator[Video, None, None]:
            # Support slices
            
            for i in range(index.start or 0,
                           index.stop  or 0,
                           index.step  or 1):
                
                yield self.get(i)
        
        return wrap()
    
    @cache
    def get(self, index: int) -> Video:
        '''
        Get a single item at an index.
        '''
        
        page = self._get_page(index // 48)
        page_index = index % 48
        
        if len(page) < page_index:
            raise IndexError('Query index out of range')

        data = page[page_index]
        
        return Video(
            core = self.core,
            url = utils.concat(consts.HOST, 'videos/hentai', data['slug'])
        )
    
    @cache
    def _get_page(self, index: int) -> list:
        '''
        Get a page at a specific index.
        '''
        
        raw = self.core.call(
            func = consts.SEARCH_API,
            method = 'POST',
            data = json.dumps(self.payload | {'page': index + 1}),
            headers = {'Content-Type': 'application/json;charset=UTF-8'}
        )
        
        return json.loads(raw.json()['hits'])

# EOF