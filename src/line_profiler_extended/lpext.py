import sys
from pathlib import Path
from types import FunctionType
from types import ModuleType
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import TextIO
from typing import Union

import line_profiler

from line_profiler_extended.utils import get_functions_from_module
from line_profiler_extended.utils import get_modules_from_path


class LineProfilerExtended(line_profiler.LineProfiler):
    def __init__(
        self,
        *items: Union[Path, ModuleType, Callable, str],
        eps: Optional[float] = None,
        include_regex: str = "",
        exclude_regex: Optional[str] = None,
    ):
        super().__init__()
        self.eps = eps if eps is not None else 0.1
        if exclude_regex is None:
            exclude_regex = r"^\."
        for item in items:
            if isinstance(item, Path):
                self.add_modules_from_path(
                    item, include_regex=include_regex, exclude_regex=exclude_regex
                )
            elif isinstance(item, str):
                self.add_modules_from_path(
                    Path(item), include_regex=include_regex, exclude_regex=exclude_regex
                )
            elif isinstance(item, ModuleType):
                self.add_module(item)
            elif isinstance(item, FunctionType):
                self.add_function(item)
            else:
                raise TypeError(f"Unsupported argument type: {type(item)}")

    def add_function(self, func: Callable) -> int:
        super().add_function(func)
        return 1

    def add_module(self, mod: ModuleType) -> int:
        nfuncsadded = 0
        for func in get_functions_from_module(mod):
            nfuncsadded += self.add_function(func)
        return nfuncsadded

    def add_modules_from_path(
        self, path: Path, include_regex: str = "", exclude_regex: str = ""
    ) -> int:
        nfuncsadded = 0
        for module in get_modules_from_path(path, include_regex, exclude_regex):
            nfuncsadded += self.add_module(module)
        return nfuncsadded

    def print_stats(
        self,
        stream: Optional[TextIO] = None,
        output_unit: Optional[Union[int, float]] = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        stats = self.get_stats()
        if stream is None:
            stream = sys.stdout
        if output_unit is not None:
            stream.write("Timer unit: %g s\n\n" % output_unit)
        else:
            stream.write("Timer unit: %g s\n\n" % stats.unit)

        for (fn, lineno, name), timings in sorted(
            stats.timings.items(), key=lambda x: float(sum(t[2] for t in x[1]))
        ):
            if sum(t[2] for t in timings) * stats.unit < self.eps:
                continue
            line_profiler.show_func(
                fn,
                lineno,
                name,
                timings,
                stats.unit,
                output_unit=output_unit,
                stream=stream,
                **kwargs,
            )
