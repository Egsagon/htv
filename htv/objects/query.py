from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

from .. import consts

if TYPE_CHECKING:
    from .. import Core

@dataclass
class Item:
    pass # TODO

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
    
    def __len__(self) -> int:
        
        return self._get_page(0).get('nbHits')
    
    def get(self, index: int) -> Item:
        '''
        Get a single item at an index.
        '''
        
        page = NotImplemented
    
    def _get_page(self, index: int) -> list:
        '''
        Get a page at a specific index.
        '''
        
        payload = self.payload | {'page': index}
        return self.core.call(consts.SEARCH_API, 'POST', payload).json()

# EOF