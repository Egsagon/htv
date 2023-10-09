'''
Constants.
'''

import re as _re
from typing import Callable, Literal

HOST = 'https://hanime.tv/'

SEARCH_API = 'https://search.htv-services.com/'

FFMPEG = 'ffmpeg -i "{input}" -bsf:a aac_adtstoasc -y -c copy {output}'

HEADERS = {
    'Accept': '*',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en,en-US',
    'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': "Windows",
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

# Those values were harverseted on dd/mm/yy: 08/10/23
search_tags = Literal[
    '3d', 'ahegao', 'anal', 'bdsm', 'big boobs', 'blow job', 'bondage', 'boob job', 'censored',
    'comedy', 'cosplay', 'creampie', 'dark skin', 'facial', 'fantasy', 'filmed', 'foot job',
    'futanari', 'gangbang', 'glasses', 'hand job', 'harem', 'hd', 'horror', 'incest', 'inflation',
    'lactation', 'loli', 'maid', 'masturbation', 'milf', 'mind break', 'mind control', 'monster',
    'nekomimi', 'ntr', 'nurse', 'orgy', 'plot', 'pov', 'pregnant', 'public sex', 'rape', 'reverse rape',
    'rimjob', 'scat', 'school girl', 'shota', 'softcore', 'swimsuit', 'teacher', 'tentacle', 'threesome',
    'toys', 'trap', 'tsundere', 'ugly bastard', 'uncensored', 'vanilla', 'virgin', 'watersports', 'x-ray',
    'yaoi', 'yuri'
]

search_brands = Literal[
    '@ oz', '37c-binetsu', 'almond collective', 'amour', 'animac', 'arms', 'blue eyes', 'bootleg',
    'breakbottle', 'bugbug', 'bunnywalker', 'celeb', 'central park media', 'chichinoya', 'chuchu',
    'circle tribute', 'cocoans', 'collaboration works', 'cosmos', 'cranberry', 'crimson', 'd3', 'daiei',
    'demodemon', 'digital works', 'discovery', 'ebimaru-do', 'echo', 'ecolonun', 'edge', 'erozuki', 'evee',
    'final fuck 7', 'five ways', 'front line', 'fruit', 'gold bear', 'gomasioken', 'green bunny',
    'hoods entertainment', 'hot bear', 'hykobo', 'jellyfish', 'jumondo', 'kate_sai', 'kenzsoft', 'king bee',
    'knack', 'kuril', 'l.', 'lemon heart', 'lilix', 'lune pictures', 'magic bus', 'magin label', 'marigold',
    'mary jane', 'media blasters', 'mediabank', 'moon rock', 'moonstone cherry', 'ms pictures', 'nihikime no dozeu',
    'nutech digital', 'pashmina', 'pink pineapple', 'pinkbell', 'pixy soft', 'pocomo premium', 'poro', 'project no.9',
    'queen bee', 'rabbit gate', 'sakamotoj', 'sandwichworks', 'schoolzone', 'seismic', 'selfish', 'seven', 'ziz',
    'shadow prod. co.', 'shinyusha', 'showten', 'soft on demand', 'stargate3d', 'studio 9 maiami', 'studio akai shohosen',
    'studio deen', 'studio fantasia', 'studio fow', 'studio ggb', 'studio zealot', 'suzuki mirano', 'syld', 't-rex', 'toho',
    'toranoana', 'tys work', 'umemaro-3d', 'union cho', 'valkyria', 'vanilla', 'white bear', 'x city', 'y.o.u.c.', 'yosino',
]

search_orders = Literal[
    'created_at_unix',
    'views',
    'likes',
    'released_at_unix',
    'title_sortable'
]


class NoResult(dict):
    
    def __repr__(self) -> str:
        return '<NO RESULT>'

EMPTY = NoResult()


def _find(raw: str, flags: int = 0) -> Callable[[str], str]:
    '''
    Single regex find wrapper.
    '''
    
    pattern = _re.compile(raw, flags)
    
    def wrap(string: str) -> str:
        results = pattern.findall(string)
        
        if len(results):
            return results[0]
        
        raise ValueError(f'Regex {pattern} failed.')

    return wrap

class re:
    '''
    Basic regexes.
    '''
    
    get_video_meta = _find(r'window.__NUXT__=({.*?});')
    get_urls = _re.compile(r'https?:\/\/.*?$', _re.M + _re.DOTALL).findall

# EOF
