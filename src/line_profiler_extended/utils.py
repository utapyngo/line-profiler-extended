import io

from line_profiler_extended.lpext import LineProfilerExtended


def get_stats(lp: LineProfilerExtended) -> str:
    stream = io.StringIO()
    lp.print_stats(stream=stream)
    return stream.getvalue()
