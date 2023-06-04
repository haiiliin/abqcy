from __future__ import annotations

import itertools
import math

import pandas as pd
import pytest
from matplotlib import pyplot as plt
from matplotlib.axes import Axes


def setAxesProps(ax: Axes, *, unpack_dict: bool = True, unpack_tuple: bool = True, **kwargs) -> None:
    for key, value in kwargs.items():
        assert hasattr(ax, key) or hasattr(ax, f"set_{key}"), f"Axes has no method {key} or set_{key}"
        method = getattr(ax, f"set_{key}") if hasattr(ax, f"set_{key}") else getattr(ax, key)
        if unpack_dict and isinstance(value, dict):
            method(**value)
        elif unpack_tuple and isinstance(value, tuple):
            method(*value)
        else:
            method(value)


@pytest.mark.parametrize(
    argnames="filepath, xcols, ycols, kwargs",
    argvalues=[
        ("outputs/element/elastic/U3.csv", "time", "U3", dict(xlabel="Time (s)", ylabel="Displacement (m)", grid=True)),
    ],
    ids=["elastic"],
)
@pytest.mark.mpl_image_compare
def test_model(
    filepath: str,
    xcols: str | list[str],
    ycols: str | list[str],
    kwargs: dict[str, ...],
):
    # Convert to list if not already
    xcols = [xcols] if not isinstance(xcols, list) else xcols
    ycols = [ycols] if not isinstance(ycols, list) else ycols
    for key in kwargs:
        kwargs[key] = [kwargs[key]] * len(xcols) if not isinstance(kwargs[key], list) else kwargs[key]
        assert len(kwargs[key]) == len(xcols), f"Length of {key} does not match number of columns"

    # Create figure
    ncols = 2 if len(xcols) > 1 else 1
    nrows = math.ceil(len(xcols) / ncols)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6 * ncols, 4 * nrows))

    # Read data and plot
    data = pd.read_csv(filepath)
    for idx, ax, xcol, ycol in zip(itertools.count(), fig.axes, xcols, ycols):
        x, y = data[xcol], data[ycol]
        ax.plot(x, y)
        for key, value in kwargs.items():
            setAxesProps(ax, **{key: value[idx]})
    fig.tight_layout()
    return fig
