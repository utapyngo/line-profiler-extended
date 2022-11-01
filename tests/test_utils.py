import sys
from functools import wraps
from pathlib import Path
from typing import Any
from typing import Callable

from line_profiler_extended.lpext import LineProfilerExtended
from line_profiler_extended.utils import get_functions_from_module
from line_profiler_extended.utils import get_modules_from_path
from line_profiler_extended.utils import get_stats

from .module import func


def decorator(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return f(*args, **kwargs)

    return wrapper


class SomeClass:
    def method(self) -> None:
        pass

    @classmethod
    @decorator
    def class_method(cls) -> None:
        pass

    @staticmethod
    @decorator
    def static_method() -> None:
        pass

    @decorator
    def decorated_method(self) -> None:
        pass


def test_get_functions_from_module() -> None:
    func_names = [
        f.__qualname__ for f in get_functions_from_module(sys.modules[__name__])
    ]
    assert func.__qualname__ in func_names
    assert SomeClass.method.__qualname__ in func_names
    assert SomeClass.class_method.__qualname__ in func_names
    assert SomeClass.static_method.__qualname__ in func_names
    assert SomeClass.decorated_method.__qualname__ in func_names


def test_get_modules_from_path() -> None:
    modules = get_modules_from_path(
        Path(__file__).parent.parent, include_regex=r"test_utils$"
    )
    assert list(modules) == [sys.modules[__name__]]


def test_get_stats() -> None:
    lp = LineProfilerExtended(eps=0.0)
    lp.add_function(func)
    stats = get_stats(lp)
    print(stats)
    assert stats.startswith("Timer unit: 1e-06 s\n\nTotal time: 0 s\nFile: ")
    assert (
        "Function: func at line 1\n"
        "\n"
        "Line #      Hits         Time  Per Hit   % Time  Line Contents\n"
        "==============================================================\n"
        "     1                                           def func() -> None:\n"
        "     2                                               pass\n"
        "\n"
    ) in stats
