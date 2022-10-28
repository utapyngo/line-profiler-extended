from line_profiler_extended.lpext import LineProfilerExtended
from line_profiler_extended.utils import get_stats


def func() -> None:
    pass


def test_get_stats() -> None:
    lp = LineProfilerExtended()
    lp.add_function(func)
    stats = get_stats(lp)
    print(stats)
    assert stats.startswith("Timer unit: 1e-06 s\n" "\n" "Total time: 0 s\n" "File: ")
    assert (
        "Function: func at line 5\n"
        "\n"
        "Line #      Hits         Time  Per Hit   % Time  Line Contents\n"
        "==============================================================\n"
        "     5                                           def func() -> None:\n"
        "     6                                               pass\n"
        "\n"
    ) in stats
