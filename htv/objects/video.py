from __future__ import annotations

import os
import json
import logging
from functools import cached_property
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from youtube_dl import YoutubeDL as downloader
from typing import TYPE_CHECKING, Any, Callable

from .. import utils
from .. import consts
from ..utils import Scheme

if TYPE_CHECKING:
    from .. import Core

logger = logging.getLogger(__name__)


@dataclass
class Producer:
    
    name: str
    id:          int = field(repr = False)
    url:         str = field(repr = False)
    email:       str = field(repr = False)
    productions: str = field(repr = False)
    avatar:      str = field(repr = False)
    slug:        str = field(repr = False)


class Video:
    '''
    Represent a video.
    '''
    
    def __init__(self, core: Core, url: str) -> None:
        '''
        Initialise a new video object.
        
        Args:
            core (Core): The core instance to use.
            url (str): The video url.
        '''
        
        self.url: str = url
        self.core = core
        self._name: str = self.url.split('/')[-1]
    
    def __repr__(self) -> str:
        return f'htv.Video({self._name})'
    
    def __str__(self) -> str:
        return self.url
    
    @cached_property
    def metadata(self) -> dict:
        '''
        Fetch the video metadata.
        '''
        
        logger.info('Fetching %s page', self)
        page = self.core.call(self.url).text
        return json.loads(consts.re.get_video_meta(page))
    
    def refresh(self) -> None:
        '''
        Refresh every video properties and attributes.
        '''
        
        # Yes its more of a reset than a refresh
        logger.info('Refreshing %s', self)
        self.__init__(self.core, self.url)
    
    def _get_scheme(self, scheme: str, sep: str = '.') -> Any:
        '''
        Get a specific scheme.
        '''
        
        if scheme.startswith('.'):
            scheme = 'state.data.video' + scheme
        
        logger.info('Fetching scheme %s', scheme)
        
        node = self.metadata
        for el in scheme.split(sep):
            node = node.get(el, consts.EMPTY)
            
        return node

    def get_M3U(self, quality: utils.Quality | str | int) -> str:
        '''
        Get the best fiting M3U URL.
        '''
        
        qualities = []
        
        for server in self.servers:
            qualities += [stream for stream in server.get('streams', [])
                          if stream.get('url')]
        
        stream = utils.Quality(quality).select({
            int(q['height']): q for q in qualities
        })
        
        logger.info('Using stream %s', stream.get('slug'))
        return stream['url']

    def download(self,
                 path: str,
                 quality: utils.Quality | str | int,
                 callback: Callable[[int, int], None] = utils.progress) -> str:
        '''
        Download the video.
        
        Args:
            path (str): The output path or directory.
            quality (Quality): The desired video quality.
        '''
        
        if os.path.isdir(path):
            # We shall not use utils.concat because it
            # only work with URLs
            path = os.path.join(path, f'{self.id}.mp4')
        
        options = {
            'outtmpl': path,
            # 'progress_hooks': [callback] # Did not work for me
            # 'external_downloader_args': ['-loglevel', 'panic']
        }
        
        with downloader(options) as ydl:
            ydl.download([self.get_M3U(quality)])
        
        return path
    
    # Video properties
    id:             int = Scheme('.hentai_video.id'                )
    franchise_id:   int = Scheme('.hentai_franchise.id'            )
    likes:          int = Scheme('.hentai_video.likes'             )
    dislikes:       int = Scheme('.hentai_video.dislikes'          )
    views:          int = Scheme('.hentai_video.views'             )
    downloads:      int = Scheme('.hentai_video.video_downloads'   )
    interests:      int = Scheme('.hentai_video.interests'         )
    title:          str = Scheme('.hentai_video.name'              )
    description:    str = Scheme('.hentai_video.description'       )
    franchise:      str = Scheme('.hentai_franchise.name'          )
    franchise_name: str = Scheme('.hentai_franchise.slug'          )
    poster:         str = Scheme('.hentai_video.poster_url'        )
    cover:          str = Scheme('.hentai_video.cover_url'         )
    storyboard:     str = Scheme('.hentai_video_storyboards'       )
    filename:       str = Scheme('.hentai_video.slug'              )
    subtitled:     bool = Scheme('.hentai_video.is_hard_subtitled' )
    censored:      bool = Scheme('.hentai_video.is_censored'       )
    servers:       list = Scheme('.videos_manifest.servers'        )
    
    # Special properties
    tags:          dict = Scheme('.hentai_video.hentai_tags',     parser = utils.arrange_tags     )
    date: datetime.date = Scheme('.hentai_video.created_at_unix', parser = datetime.fromtimestamp )
    duration: timedelta = Scheme('.hentai_video.duration_in_ms',  parser = utils.to_delta         )
    
    @cached_property
    def producer(self) -> Producer:
        '''
        The video producer.
        '''
    
        return Producer(
            name        = self._get_scheme('.brand.title'      ),
            url         = self._get_scheme('.brand.website_url'),
            id          = self._get_scheme('.brand.id'         ),
            email       = self._get_scheme('.brand.email'      ),
            productions = self._get_scheme('.brand.count'      ),
            avatar      = self._get_scheme('.brand.logo_url'   ),
            slug        = self._get_scheme('.brand.slug'       )
        )

# EOF