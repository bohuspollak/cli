"""
nextstrain.org remote.

Backend module for the remote family of commands.
"""

import requests
import urllib.parse
from pathlib import Path
from typing import Iterable

def ls(url: urllib.parse.ParseResult) -> Iterable[Path]:
    """
    List the files deployed at the given remote *url*.
    """
    path = url.path.replace('nextstrain.org', '')

    # TODO use charon v2 when implemented, e.g.
    # request = requests.get('https://nextstrain.org/charon/v2/dataset/%s' % path)
    request = requests.get('http://localhost:5000/charon/getAvailable?prefix=%s' % path)
    request.raise_for_status()

    json = request.json()

    return [ dataset['request'] for dataset in json['datasets'] ]
