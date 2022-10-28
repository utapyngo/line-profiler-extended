from typing import Dict
from typing import Optional

from _pytest.config import Config
from _pytest.mark import Mark
from _pytest.python import Function
from _pytest.terminal import TerminalReporter

from line_profiler_extended.lpext import LineProfilerExtended
from line_profiler_extended.utils import get_stats


def pytest_runtest_call(item: Function) -> None:
    marker: Optional[Mark] = item.get_closest_marker("line_profile")
    if not marker:
        return
    lp = LineProfilerExtended(*marker.args, **marker.kwargs)
    item_runtest = item.runtest

    # noinspection PyProtectedMember
    def runtest() -> None:
        lp.runcall(item_runtest)
        stats: Dict[str, str] = getattr(item.config, "_line_profile", {})
        stats[item.nodeid] = get_stats(lp)
        item.config._line_profile = stats  # type: ignore

    item.runtest = runtest  # type: ignore


def pytest_terminal_summary(terminalreporter: TerminalReporter, config: Config) -> None:
    reports: Dict[str, str] = getattr(config, "_line_profile", {})
    for k, v in reports.items():
        terminalreporter.write_sep("=", f"Line profile result for {k}")
        terminalreporter.write(v)


def pytest_configure(config: Config) -> None:
    config.addinivalue_line("markers", "line_profile: Line profile this test")
