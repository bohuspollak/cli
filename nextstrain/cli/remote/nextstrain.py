"""
nextstrain.org remote.

Backend module for the remote family of commands.

TODO should support non-groups nextstrain.org URLs?
"""

import os
import re
import json
import requests
import urllib.parse
from pathlib import Path
from typing import Iterable, Tuple
from ..gzip import ContentDecodingWriter


def download(url: urllib.parse.ParseResult, local_path: Path, recursively: bool = False) -> Iterable[Tuple[Path, Path]]:
    """
    Download the files deployed at the given remote *url*, optionally
    *recursively*, saving them into the *local_dir*.

    TODO 500 error when file doesn't exist

    TODO how to handle when referencing directory without recursive option? issue exists for S3
    currently throws a JSONDecodeError.
    """
    path = url.path.replace('nextstrain.org/', '')

    # TODO use charon v2 when implemented, e.g.
    # request = requests.get('https://nextstrain.org/charon/v2/dataset/%s' % path)

    if recursively:
        # TODO add recursive support
        pass
    else:
        request = requests.get('http://localhost:5000/charon/getDataset?prefix=%s' % path)
        request.raise_for_status()

        objects = [ request ]

    path_with_ext = path + '.json'  # TODO

    def local_file_path(obj):
        if local_path.is_dir():
            return local_path / path_with_ext
        else:
            return local_path

    files = list(zip(objects, [local_file_path(obj) for obj in objects]))


    for remote_object, local_file in files:
        yield Path(path_with_ext), local_file

        # Match the URL prefix beginning with "/groups/{group-name}/{optional-dir-name}/"
        path_prefix = re.match(
            r'groups\/([\w-]*\/*)*\/(?=[\w-]*.[\w-]*$)', path_with_ext)[0]

        os.makedirs(path_prefix, exist_ok=True)

        # TODO encoding
        with open(local_file, "w") as file:
            file.write(json.dumps(remote_object.json()))


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
