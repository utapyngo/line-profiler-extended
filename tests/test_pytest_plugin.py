import pytest
from _pytest.pytester import Pytester


@pytest.mark.order("last")
def test_mark(pytester: Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest

        @pytest.mark.line_profile
        def test_mark() -> None:
            pass
        """
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
    result.stdout.fnmatch_lines(
        [
            "=============== Line profile result for test_mark.py::test_mark ================",
            "Timer unit: 1e-06 s",
        ]
    )
