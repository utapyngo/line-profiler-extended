from .lpext import LineProfilerExtended

__all__ = ["LineProfilerExtended"]

try:
    from .ipython_extension import load_ipython_extension

    __all__ += ["load_ipython_extension"]  # pragma: no cover
except ImportError:
    pass
