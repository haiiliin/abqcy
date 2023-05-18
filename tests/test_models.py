import pandas as pd
import pytest
from matplotlib import pyplot as plt


@pytest.mark.parametrize(
    argnames="data_path, xcol, ycol, xlabel, ylabel",
    argvalues=[("outputs/element/elastic/U3.csv", "time", "U3", "Time (s)", "Displacement (m)")],
    ids=["elastic"],
)
@pytest.mark.mpl_image_compare
def test_model(data_path: str, xcol: str, ycol: str, xlabel: str, ylabel: str):
    data = pd.read_csv(data_path)
    x, y = data[xcol], data[ycol]
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()
    return fig
