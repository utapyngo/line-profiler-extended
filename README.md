# line-profiler-extended

[![PyPI](https://img.shields.io/pypi/v/line-profiler-extended?style=flat-square)](https://pypi.python.org/pypi/line-profiler-extended/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/line-profiler-extended?style=flat-square)](https://pypi.python.org/pypi/line-profiler-extended/)
[![PyPI - License](https://img.shields.io/pypi/l/line-profiler-extended?style=flat-square)](https://pypi.python.org/pypi/line-profiler-extended/)
[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)


---

**Documentation**: [https://utapyngo.github.io/line-profiler-extended](https://utapyngo.github.io/line-profiler-extended)

**Source Code**: [https://github.com/utapyngo/line-profiler-extended](https://github.com/utapyngo/line-profiler-extended)

**PyPI**: [https://pypi.org/project/line-profiler-extended/](https://pypi.org/project/line-profiler-extended/)

---

Inherits awesome rkern's line-profiler and adds some useful features.

## Installation

```sh
pip install line-profiler-extended
```

## Using the API

```python
from line_profiler_extended import LineProfilerExtended

def foo():
    pass

# profile the foo function
profiler = LineProfilerExtended(foo)

# profile all functions from some_module
import some_module
profiler = LineProfilerExtended(some_module)

# profile all functions from all modules found recursively
# starting from the grandparent directory of the current file
from pathlib import Path
profiler = LineProfilerExtended(Path(__file__).parent.parent)

# profile all functions from all modules found recursively in "path",
# reporting only functions that took at least 1 millisecond
profiler = LineProfilerExtended("path", eps=0.001)

# profile all functions from all modules found recursively in "path" with "m" in module name but without "mm"
profiler = LineProfilerExtended("path", include_regex="m", exclude_regex="mm")

# all types of locations can be combined
profiler = LineProfilerExtended(
    Path("/some/path"), "path", some_module, foo,
    eps=0.001, include_regex="m", exclude_regex="mm"
)

profiler.enable_by_count()
profiler.runcall(foo)
profiler.print_stats()
```

## Usage with IPython

```ipython
%load_ext line_profiler_extended

# profile the foo function
%lpext -p foo foo()

# profile all functions from some_module
%lpext -p some_module foo()

# profile all functions from all modules found recursively in some path
from pathlib import Path
%lpext -p Path("/some/path") foo()

# profile all functions from all modules found recursively in "path",
# reporting only functions that took at least 1 millisecond
%lpext -p "path" --eps 0.001 foo()

# profile all functions from all modules found recursively in "path" with "m" in module name but without "mm"
%lpext -p "path" --include "m" --exclude "mm" foo()

# all types of locations can be combined
%lpext -p Path(__file__).parent.parent -p "path" -p some_module -p foo --eps 0.001 --include "m" --exclude "mm" foo()
```

## Usage with pytest

```python
import pytest
from pathlib import Path

# all args are passed directly to the LineProfilerExtended constructor
@pytest.mark.line_profile.with_args(Path(__file__).parent.parent, eps=0.01)
def test_foo():
    pass
```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.7+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github project page
 ](https://pages.github.com/) automatically as part each release.

### Releasing

Trigger the [Draft release workflow](https://github.com/utapyngo/line-profiler-extended/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/utapyngo/line-profiler-extended/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/utapyngo/line-profiler-extended/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

This project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
