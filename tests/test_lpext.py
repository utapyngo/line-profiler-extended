from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture
from pytest_mock import MockerFixture

from line_profiler_extended.lpext import LineProfilerExtended
from tests import module


class TestLineProfilerExtended:
    def test_init_eps(self) -> None:
        lp = LineProfilerExtended()
        assert lp.eps == 0.1

        lp = LineProfilerExtended(eps=0.0)
        assert lp.eps == 0.0

    def test_init_exclude_regex(self, mocker: MockerFixture) -> None:
        add_modules_from_path = mocker.patch.object(
            LineProfilerExtended, "add_modules_from_path"
        )
        exclude_regex = r"^\.|conftest$|__init__|^src|test_pytest_plugin$"
        LineProfilerExtended(Path(__file__).parent.parent, exclude_regex=exclude_regex)
        add_modules_from_path.assert_called_once_with(
            Path(__file__).parent.parent, include_regex="", exclude_regex=exclude_regex
        )

    def test_init_str_path_exclude_regex(self, mocker: MockerFixture) -> None:
        add_modules_from_path = mocker.patch.object(
            LineProfilerExtended, "add_modules_from_path"
        )
        exclude_regex = r"^\.|conftest$|__init__|^src|test_pytest_plugin$"
        LineProfilerExtended("..", exclude_regex=exclude_regex)
        add_modules_from_path.assert_called_once_with(
            Path(".."), include_regex="", exclude_regex=exclude_regex
        )

    def test_init_multiple_args(self, mocker: MockerFixture) -> None:
        add_modules_from_path = mocker.patch.object(
            LineProfilerExtended, "add_modules_from_path"
        )
        add_module = mocker.patch.object(LineProfilerExtended, "add_module")
        add_function = mocker.patch.object(LineProfilerExtended, "add_function")

        LineProfilerExtended(Path(__file__).parent.parent, "..", module, module.func)
        add_module.assert_called_with(module)
        add_function.assert_called_with(module.func)
        add_modules_from_path.assert_any_call(
            Path(".."), include_regex="", exclude_regex=r"^\."
        )
        add_modules_from_path.assert_any_call(
            Path(__file__).parent.parent, include_regex="", exclude_regex=r"^\."
        )

    def test_init_unsupported_type(self) -> None:
        with pytest.raises(TypeError):
            LineProfilerExtended(1)  # type: ignore

    def test_add_modules_from_path(self) -> None:
        lp = LineProfilerExtended()
        assert (
            lp.add_modules_from_path(Path(__file__).parent.parent, exclude_regex=r"^\.")
            > 0
        )

    def test_print_stats(self, capsys: CaptureFixture) -> None:
        lp = LineProfilerExtended(module, eps=1)
        lp.print_stats(output_unit=1)
        output = capsys.readouterr().out
        assert "Timer unit: 1 s\n" in output
