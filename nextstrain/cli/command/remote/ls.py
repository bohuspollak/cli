"""
List pathogen JSON data files or Markdown narratives on a remote source.
URLs support optional path prefixes for restricting the files listed.

    nextstrain remote list s3://my-bucket/some/prefix/

or

    nextstrain remote list nextstrain.org/groups/some/prefix/

will list files named "some/prefix/*".

See `nextstrain remote --help` for more information on remote sources.
"""

from urllib.parse import urlparse
from ...remote import s3, nextstrain
from ...util import warn


SUPPORTED_SCHEMES = {
    "s3": s3,
    "": nextstrain,
}


def register_parser(subparser):
    parser = subparser.add_parser(
        "list",
        aliases = ["ls"],
        help    = "List dataset and narrative files")

    parser.add_argument(
        "remote_path",
        help    = "Remote path as a URL, with optional key/path prefix",
        metavar = "<nextstrain.org/groups/group-name/> or <s3://bucket-name>")

    return parser


def run(opts):
    url = urlparse(opts.remote_path)

    if not url.scheme and not url.path.startswith('nextstrain.org'):
        warn("Error. Unsupported URL path %s" % url.path)
        warn("")
        warn("Only nextstrain.org paths or s3:// URLs are supported.")
        return 1

    elif url.scheme and url.scheme not in SUPPORTED_SCHEMES:
        warn("Error: Unsupported remote scheme %s://" % url.scheme)
        warn("")
        warn("Supported schemes are: %s" % ", ".join(SUPPORTED_SCHEMES))
        return 1

    remote = SUPPORTED_SCHEMES[url.scheme]

    files = remote.ls(url)

    for file in files:
        print(file)

    return 0
