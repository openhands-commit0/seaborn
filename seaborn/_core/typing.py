from __future__ import annotations
from collections.abc import Iterable, Mapping
from datetime import date, datetime, timedelta
from typing import Any, Optional, Union, Tuple, List, Dict
from numpy import ndarray
from pandas import Series, Index, Timestamp, Timedelta
from matplotlib.colors import Colormap, Normalize
ColumnName = Union[str, bytes, date, datetime, timedelta, bool, complex, Timestamp, Timedelta]
Vector = Union[Series, Index, ndarray]
VariableSpec = Union[ColumnName, Vector, None]
VariableSpecList = Union[List[VariableSpec], Index, None]
DataSource = Union[object, Mapping, None]
OrderSpec = Union[Iterable, None]
NormSpec = Union[Tuple[Optional[float], Optional[float]], Normalize, None]
PaletteSpec = Union[str, list, dict, Colormap, None]
DiscreteValueSpec = Union[dict, list, None]
ContinuousValueSpec = Union[Tuple[float, float], List[float], Dict[Any, float], None]

class Default:

    def __repr__(self):
        return '<default>'

class Deprecated:

    def __repr__(self):
        return '<deprecated>'
default = Default()
deprecated = Deprecated()