# HTV API

Low effort API for the HTV website (its a hentai website).

This was made in the context of a web-scrapping speedrun.
Expect bugs and lack of support towards this project. 

## Installation

```sh
pip install git+https://github.com/Egsagon.htv.git
```

## Usage

### Fetch video data

Video properties are `htv.Schema` properties. They use a cache system.
They can be refreshed all at once using `video.refresh()`.

```py
>>> import htv

# Initialise a core
>>> core = htv.Core()

# Fetch a video
>>> video = core.get('...') # Video URL or slug

# View video information
>>> video.title
>>> video.likes
# etc.
```

#### Available video properties

| Property               | Type       | Description                         |
| ---------------------- | ---------- | ----------------------------------- |
| `video.title`          | `str`      | Video title.                        |
| `video.description`    | `str`      | Video description.                  |
| `video.id`             | `int`      | Internal video id.                  |
| `video.likes`          | `int`      | Number of likes.                    |
| `video.dislikes`       | `int`      | Number of dislikes.                 |
| `video.views`          | `int`      | Number of views.                    |
| `video.downloads`      | `int`      | Number of downloads.                |
| `video.interests`      | `int`      | Number of interests.                |
| `video.poster`         | `str`      | Video poster URL.                   |
| `video.cover`          | `str`      | Video cover URL.                    |
| `video.storyboard`     | `str`      | Video storyboard URL.               |
| `video.filename`       | `str`      | Video raw name ('slug').            |
| `video.subtitled`      | `bool`     | Wether video has subtitles embeded. |
| `video.censored`       | `bool`     | Wether video is marked as censored. |
| `video.franchise`      | `str`      | Video franchise name.               |
| `video.franchise_id`   | `int`      | Internal video franchise id.        |
| `video.franchise_name` | `str`      | Raw video franchise name.           |
| `video.servers`        | `list`     | List of CDNs. Used internally.      |
| `video.tags`           | `dict`     | Video tags.                         |
| `video.date`           | `date`     | Video release date.                 |
| `video.duration`       | `delta`    | Video duration as timedelta object. |
| `video.producer`       | `Producer` | Object representing video producer. |

#### Available video producer properties

| Name                   | Type  | Description                |
| ---------------------- | ----- | -------------------------- |
| `producer.name`        | `str` | Producer name.             |
| `producer.url`         | `str` | Producer URL.              |
| `producer.id`          | `int` | Producer internal id.      |
| `producer.email`       | `str` | Producer email (if given). |
| `producer.productions` | `int` | Producer production count. |
| `producer.avatar`      | `str` | Producer avatar URL.       |
| `producer.slug`        | `str` | Producer raw name.         |

### Search for videos

To search for videos you can generate a query object,
which will manage and cache requests sent to the server. 

```py
import htv

core = htv.Core()

# Initialise the query
query = core.search(
    'my query',       # Search string
    tags = ...,       # Tags to search with
    tags_mode = ...,  # Tags mode
                      # - 'AND' => Videos must have all specified tags
                      # - 'OR' => Videos can have any specified tag
    brands = ...,     # Brands to search videos from
    blacklist = ...,  # Blacklisted tags
    order = ...,      # Video order
    ordering = ...    # Video ordering direction
                      # - '+' => Ascending order
                      # - '-' => Descending order
)

# Enumerate for all videos
for video in query:
    print(video)

# Enumerate for a range of videos
for video in query[:10]:
    print(video)

# Get a single video
my_video = query[0]
```

### Downloading a video

You can download a video using the YoutubeDL implementation.

```py
import htv
from htv import Quality

core = htv.Core()

video = core.get('...')

video.download(
    path = '.', # Can be a directory or a existing/non-existing file.
    quality = Quality.BEST # or literal values: 'best', 'worst', 1080, etc.
)
```

For advanced video downloading, you can use the `video.get_M3U` method.

```py
import os

core = ...
video = ...

m3u = video.get_M3U(quality = Quality.BEST)

# Do something with the file, e.g. save it
with open('my-video.m3u8', 'wb') as file:
    
    raw = core.call(m3u).content
    file.write(raw)

```

### Further usage

For more information about this project, you might want to read
the project source code docstrings.

All tags, categories, brands and constants of any kind are stored
inside Literals so you can use static type hints to type them
faster. The used types can be found inside the `htv/consts.py` file.

## License

This project is under the `GPLv3` license. See the `LICENSE` file.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
