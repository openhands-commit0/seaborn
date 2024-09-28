from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd
from seaborn._stats.base import Stat

@dataclass
class PolyFit(Stat):
    """
    Fit a polynomial of the given order and resample data onto predicted curve.
    """
    order: int = 2
    gridsize: int = 100

    def __call__(self, data, groupby, orient, scales):
        return groupby.apply(data.dropna(subset=['x', 'y']), self._fit_predict)

@dataclass
class OLSFit(Stat):
    ...