from __future__ import annotations
import warnings
from collections import UserString
from numbers import Number
from datetime import datetime
import numpy as np
import pandas as pd
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Literal
    from pandas import Series

class VarType(UserString):
    """
    Prevent comparisons elsewhere in the library from using the wrong name.

    Errors are simple assertions because users should not be able to trigger
    them. If that changes, they should be more verbose.

    """
    allowed = ('numeric', 'datetime', 'categorical', 'boolean', 'unknown')

    def __init__(self, data):
        assert data in self.allowed, data
        super().__init__(data)

    def __eq__(self, other):
        assert other in self.allowed, other
        return self.data == other

def variable_type(vector: Series, boolean_type: Literal['numeric', 'categorical', 'boolean']='numeric', strict_boolean: bool=False) -> VarType:
    """
    Determine whether a vector contains numeric, categorical, or datetime data.

    This function differs from the pandas typing API in a few ways:

    - Python sequences or object-typed PyData objects are considered numeric if
      all of their entries are numeric.
    - String or mixed-type data are considered categorical even if not
      explicitly represented as a :class:`pandas.api.types.CategoricalDtype`.
    - There is some flexibility about how to treat binary / boolean data.

    Parameters
    ----------
    vector : :func:`pandas.Series`, :func:`numpy.ndarray`, or Python sequence
        Input data to test.
    boolean_type : 'numeric', 'categorical', or 'boolean'
        Type to use for vectors containing only 0s and 1s (and NAs).
    strict_boolean : bool
        If True, only consider data to be boolean when the dtype is bool or Boolean.

    Returns
    -------
    var_type : 'numeric', 'categorical', or 'datetime'
        Name identifying the type of data in the vector.
    """
    pass

def categorical_order(vector: Series, order: list | None=None) -> list:
    """
    Return a list of unique data values using seaborn's ordering rules.

    Parameters
    ----------
    vector : Series
        Vector of "categorical" values
    order : list
        Desired order of category levels to override the order determined
        from the `data` object.

    Returns
    -------
    order : list
        Ordered list of category levels not including null values.

    """
    pass