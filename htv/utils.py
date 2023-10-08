'''
Utilities.
'''

from datetime import timedelta
from typing import Literal, Self, Any, Callable

def concat(*args) -> str:
    '''
    Concatenate URL (NOT path files).
    '''
    
    return '/'.join(map(lambda e: e.strip('/'), args))

def progress(current, total) -> None:
    '''
    Simple display progress.
    '''
    
    percent = round((current / total) * 100)
    
    print(f'Downloading: \033[92m{percent}\033[0m% [\033[93m{current}/{total}\033[0m]',
          end = '\r')
    
    # Display newline after finish
    if current == total: print()

def arrange_tags(tags: list[dict]) -> dict[int, str]:
    '''
    Arrange video tags in a more pythonic way.
    '''
    
    return {tag['id']: tag['text'] for tag in tags}

def to_delta(ms: int) -> timedelta:
    '''
    Convert milliseconds to a timedelta object.
    '''
    
    return timedelta(milliseconds = ms)

def closest(numbers: list[int], value: int) -> int:
    '''
    Find the closest value in a list to the given value.

    Args:
        numbers (list[int]): List of possible values.
        value (int): Target value.

    Returns:
        int: The closest value in the list to the target value.
    '''
    
    return min(numbers, key = lambda el: abs(el - value))

class _BaseQuality:
    '''
    Represents a constant quality object that can selects
    itself among a list of qualities.
    '''
    
    def __init__(self, value: Literal['best', 'half', 'worst'] | int | Self) -> None:
        '''
        Initialise a new quality object.
        
        Args:
            value (Literal['best', 'half', 'worst'] | int | Self): String, number or quality object to initialise from.
        '''
        
        self.value = value
        
        if isinstance(value, _BaseQuality):
            self.value = value.value
        
        if isinstance(self.value, str):
            assert self.value.lower() in ('best', 'half', 'worst')
    
    def select(self, qualities: dict) -> str:
        '''
        Select among a list of qualities.
        
        Args:
            quals (dict): A dict containing qualities and URLs.
        
        Returns:
            str: The chosen quality URL.
        '''
        
        keys = list(qualities.keys())
        
        if isinstance(self.value, str):
            # Get approximative quality
            
            if self.value == 'best': return qualities[max(keys)]
            elif self.value == 'worst': return qualities[min(keys)]
            else: return qualities[ sorted(keys)[ len(keys) // 2 ] ]
        
        elif isinstance(self.value, int):
            # Get exact quality or nearest
            
            if (s:= str(self.value)) in keys: return qualities[s]
            else: return qualities[closest(keys, self.value)]
        
        # This should not happen
        raise TypeError('Internal error: quality type is', type(self.value))

class Quality(_BaseQuality):
    
    BEST =  _BaseQuality('best')
    HALF =  _BaseQuality('half')
    WORST = _BaseQuality('worst')

class Scheme:
    '''
    Represents a schema property.
    '''
    
    def __init__(self, scheme: str, sep: str = '.', parser: Callable = None) -> None:
        
        self.scheme = scheme
        self.parser = parser
        self.sep = sep
        self.value = None

    def __get__(self, instance, owner) -> Any:
        
        if not self.value:
            self.value = instance._get_scheme(self.scheme, self.sep)
            
            if self.parser:
                self.value = self.parser(self.value)
        
        return self.value

# EOF