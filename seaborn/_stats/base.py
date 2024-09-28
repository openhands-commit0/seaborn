"""Base module for statistical transformations."""
from __future__ import annotations
from collections.abc import Iterable
from dataclasses import dataclass
from typing import ClassVar, Any
import warnings
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pandas import DataFrame
    from seaborn._core.groupby import GroupBy
    from seaborn._core.scales import Scale

@dataclass
class Stat:
    """Base class for objects that apply statistical transformations."""
    group_by_orient: ClassVar[bool] = False

    def _check_param_one_of(self, param: str, options: Iterable[Any]) -> None:
        """Raise when parameter value is not one of a specified set."""
        pass

    def _check_grouping_vars(self, param: str, data_vars: list[str], stacklevel: int=2) -> None:
        """Warn if vars are named in parameter without being present in the data."""
        pass

    def __call__(self, data: DataFrame, groupby: GroupBy, orient: str, scales: dict[str, Scale]) -> DataFrame:
        """Apply statistical transform to data subgroups and return combined result."""
        return data