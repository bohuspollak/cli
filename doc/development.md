# Development

Development of `nextstrain-cli` happens at <https://github.com/nextstrain/cli>.

We currently target compatibility with Python 3.5 and higher.  This may be
increased to 3.6 in the future.

Versions for this project follow the [Semantic Versioning rules][].

## Setup

You can use [Pipenv](https://pipenv.pypa.io) to spin up an isolated development
environment:

    pipenv sync --dev
    pipenv run nextstrain --help

The Pipenv development environment includes our dev tools (described below):

    pipenv run pytest           # runs doctests as well as mypy and flake8
    pipenv run mypy nextstrain
    pipenv run flake8

## Running with local changes

From within a clone of the git repository you can run `./bin/nextstrain` to
test your local changes without installing them.  (Note that `./bin/nextstrain`
is not the script that gets installed by pip as `nextstrain`; that script is
generated by the `entry_points` configuration in `setup.py`.)

## Releasing

New releases are made frequently and tagged in git using a [_signed_ tag][].
The source and wheel (binary) distributions are uploaded to [the nextstrain-cli
project on PyPi](https://pypi.org/project/nextstrain-cli).

There is a `./devel/release` script which will prepare a new release from your
local repository.  It ends with instructions for you on how to push the release
commit/tag and how to upload the built distributions to PyPi.  You'll need [a
PyPi account][] and [twine][] installed.

## Tests

Tests are run with [pytest](https://pytest.org).  To run everything, use:

    pytest

This includes the type annotation and static analysis checks described below.

## Type annotations and static analysis

Our goal is to gradually add [type annotations][] to our code so that we can
catch errors earlier and be explicit about the interfaces expected and
provided.  Annotation pairs well with the functional approach taken by the
package.

During development you can run static type checks using [mypy][]:

    $ mypy nextstrain
    # No output is good!

There are also many [editor integrations for mypy][].

Note that our goal of compatibility with Python 3.5 means that type comments
are necessary to annotate variable declarations:

    # Not available in Python 3.5:
    foo: int = 3

    # Instead, use trailing type hint comments:
    foo = 3  # type: int

The [`typing_extensions`][] module should be used for features added to the
standard `typings` module after 3.5.  (Currently this isn't necessary since we
don't use those features.)

We also use [Flake8][] for some static analysis checks focusing on runtime
safety and correctness.  You can run them like this:

    $ flake8
    # No output is good!


[Semantic Versioning rules]: https://semver.org
[_signed_ tag]: https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work
[a PyPi account]: https://pypi.org/account/register/
[twine]: https://pypi.org/project/twine
[type annotations]: https://www.python.org/dev/peps/pep-0484/
[mypy]: http://mypy-lang.org/
[editor integrations for mypy]: https://github.com/python/mypy#ide--linter-integrations
[`typing_extensions`]: https://pypi.org/project/typing-extensions
[Flake8]: https://flake8.pycqa.org
