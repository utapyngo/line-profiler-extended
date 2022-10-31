import pytest
from _pytest.pytester import Pytester


@pytest.mark.order("last")
def test_mark(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest

        import module1
        from module2 import func2

        @pytest.mark.line_profile.with_args(module1, func2, eps=0.0001)
        def test_mark() -> None:
            module1.func()
            func2()
        """,
        module1="""
        import time
        def func() -> None:
            time.sleep(0.01)
        """,
        module2="""
        import time
        def func2() -> None:
            time.sleep(0.01)
        """,
    )
    result = pytester.runpytest()
    print(result.stdout.str())
    result.stdout.fnmatch_lines(
        [
            "=============== Line profile result for test_mark.py::test_mark ================",
            "Timer unit: 1e-06 s",
        ]
    )
    result.stdout.fnmatch_lines(
        [
            "Function: func at line 2",
            "Line #      Hits         Time  Per Hit   % Time  Line Contents",
            "==============================================================",
            "     2                                           def func() -> None:",
        ]
    )
    result.stdout.fnmatch_lines(
        [
            "Function: func2 at line 2",
            "Line #      Hits         Time  Per Hit   % Time  Line Contents",
            "==============================================================",
            "     2                                           def func2() -> None:",
        ]
    )
    result.assert_outcomes(passed=1)
