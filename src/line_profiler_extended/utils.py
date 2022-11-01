import importlib
import io
import os
import re
from inspect import isclass
from inspect import isfunction
from pathlib import Path
from types import ModuleType
from typing import Callable
from typing import Iterator

from line_profiler import LineProfiler


def get_modules_from_path(
    path: Path, include_regex: str = "", exclude_regex: str = ""
) -> Iterator[ModuleType]:
    cwd = os.getcwd()
    os.chdir(path)
    for p in path.glob("**/*.py"):
        module_name = str(p.relative_to(path).with_suffix("")).replace("/", ".")
        if include_regex and not re.search(include_regex, module_name):
            continue
        if exclude_regex and re.search(exclude_regex, module_name):
            continue
        yield importlib.import_module(module_name)
    os.chdir(cwd)


def get_functions_from_module(mod: ModuleType) -> Iterator[Callable]:
    for item in mod.__dict__.values():
        if isclass(item):
            for v in item.__dict__.values():
                if isfunction(v):
                    yield v
                elif hasattr(v, "__func__") and isfunction(v.__func__):
                    yield v.__func__
        elif isfunction(item):
            yield item


def get_stats(lp: LineProfiler) -> str:
    stream = io.StringIO()
    lp.print_stats(stream=stream)
    return stream.getvalue()
