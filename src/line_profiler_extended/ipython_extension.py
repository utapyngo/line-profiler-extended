from io import StringIO
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

from IPython import InteractiveShell
from IPython.core.error import UsageError
from IPython.core.magic import Magics
from IPython.core.magic import line_magic
from IPython.core.magic import magics_class
from IPython.core.page import page
from IPython.utils.ipstruct import Struct

from .lpext import LineProfilerExtended


@magics_class
class LineProfilerMagics(Magics):
    @line_magic
    def lpext(self, line: str = "") -> Optional[LineProfilerExtended]:
        """Execute a statement under the line-by-line profiler from the
        line_profiler module.

        Usage:
        %lpext -p "path" -p pathlib.Path("path") -p module -p func --eps 0.01 --include .* --exclude venv <statement>

        The given statement (which doesn't require quote marks) is run via the
        LineProfiler. Profiling is enabled for the functions specified by the -f
        options. The statistics will be shown side-by-side with the code through the
        pager once the statement has completed.

        Options:

        -p <path>: profile all functions found in the given path.
        -p <module>: profile all functions found in the given module.
        -p <function>: profile the given function.
        Multiple -p options may be used. The argument may be any expression that gives
        a Python function, method, module or path (either pathlib.Path or str).
        However, one must be careful to avoid
        spaces that may confuse the option parser.

        One or more -p option is required to get any useful results.

        -eps <float>: specify the minimum execution time in seconds to be considered
        for profiling. Default is 0.1.

        -include <regex>: specify a regex to include modules in profiling.
        All modules are included by default.

        -exclude <regex>: specify a regex to exclude modules from profiling.
        Default value: "^\\.", i.e. exclude all modules starting with a dot.

        -D <filename>: dump the raw statistics out to a pickle file on disk. The
        usual extension for this is ".lprof". These statistics may be viewed later
        by running line_profiler.py as a script.

        -T <filename>: dump the text-formatted statistics with the code side-by-side
        out to a text file.

        -r: return the LineProfiler object after it has completed profiling.

        -u: specify time unit for the print-out in seconds.
        """

        # Escape quote markers.
        opts_def = Struct(
            D=[""], T=[""], p=[], u=None, eps=[None], include=[""], exclude=[None]
        )
        line = line.replace('"', r"\"").replace("'", r"\'")
        opts, arg_str = self.parse_options(
            line, "rp:D:T:u:", "eps=", "include=", "exclude=", list_all=True
        )
        opts.merge(opts_def)

        eps = None
        if opts.eps[0] is not None:
            eps = float(opts.eps[0])

        profile = LineProfilerExtended(
            *self._eval_args(opts.p),
            eps=eps,
            include_regex=opts.include[0],
            exclude_regex=opts.exclude[0],
        )

        if opts.u is not None:
            try:
                output_unit = float(opts.u[0])
            except Exception:
                raise TypeError("Timer unit setting must be a float.")
        else:
            output_unit = None

        message, output = self._run(arg_str, output_unit, profile)

        dump_file = opts.D[0]
        if dump_file:
            profile.dump_stats(dump_file)
            print(f"\n*** Profile stats pickled to file {dump_file!r}. {message}")

        text_file = opts.T[0]
        if text_file:
            pfile = open(text_file, "w")
            pfile.write(output)
            pfile.close()
            print(f"\n*** Profile printout saved to text file {text_file!r}. {message}")

        return_value = None
        if "r" in opts:
            return_value = profile

        return return_value

    def _eval_args(self, p: List[str]) -> List[Any]:
        global_ns = self.shell.user_global_ns
        local_ns = self.shell.user_ns
        args = []
        for name in p:
            try:
                args.append(eval(name, global_ns, local_ns))
            except Exception as e:
                raise UsageError(
                    f"Could not eval path, module, or function {name}.\n{e.__class__.__name__}: {e}"
                )
        return args

    def _run(
        self, arg_str: str, output_unit: Optional[float], profile: LineProfilerExtended
    ) -> Tuple[str, str]:
        global_ns = self.shell.user_global_ns
        local_ns = self.shell.user_ns

        # Add the profiler to the builtins for @profile.
        import builtins

        if "profile" in builtins.__dict__:
            had_profile = True
            old_profile = builtins.__dict__["profile"]
        else:
            had_profile = False
            old_profile = None
        builtins.__dict__["profile"] = profile
        try:
            try:
                profile.runctx(arg_str, global_ns, local_ns)
                message = ""
            except SystemExit:
                message = """*** SystemExit exception caught in code being profiled."""
            except KeyboardInterrupt:
                message = (
                    "*** KeyboardInterrupt exception caught in code being " "profiled."
                )
        finally:
            if had_profile:
                builtins.__dict__["profile"] = old_profile
        # Trap text output.
        stdout_trap = StringIO()
        profile.print_stats(stdout_trap, output_unit=output_unit)
        output = stdout_trap.getvalue()
        output = output.rstrip()
        page(output)
        print(message, end="")
        return message, output


def load_ipython_extension(ipython: InteractiveShell) -> None:
    ipython.register_magics(LineProfilerMagics)
