from __future__ import annotations
from collections.abc import Generator
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from seaborn._core.plot import FacetSpec, PairSpec
    from matplotlib.figure import SubFigure

class Subplots:
    """
    Interface for creating and using matplotlib subplots based on seaborn parameters.

    Parameters
    ----------
    subplot_spec : dict
        Keyword args for :meth:`matplotlib.figure.Figure.subplots`.
    facet_spec : dict
        Parameters that control subplot faceting.
    pair_spec : dict
        Parameters that control subplot pairing.
    data : PlotData
        Data used to define figure setup.

    """

    def __init__(self, subplot_spec: dict, facet_spec: FacetSpec, pair_spec: PairSpec):
        self.subplot_spec = subplot_spec
        self._check_dimension_uniqueness(facet_spec, pair_spec)
        self._determine_grid_dimensions(facet_spec, pair_spec)
        self._handle_wrapping(facet_spec, pair_spec)
        self._determine_axis_sharing(pair_spec)

    def _check_dimension_uniqueness(self, facet_spec: FacetSpec, pair_spec: PairSpec) -> None:
        """Reject specs that pair and facet on (or wrap to) same figure dimension."""
        pass

    def _determine_grid_dimensions(self, facet_spec: FacetSpec, pair_spec: PairSpec) -> None:
        """Parse faceting and pairing information to define figure structure."""
        pass

    def _handle_wrapping(self, facet_spec: FacetSpec, pair_spec: PairSpec) -> None:
        """Update figure structure parameters based on facet/pair wrapping."""
        pass

    def _determine_axis_sharing(self, pair_spec: PairSpec) -> None:
        """Update subplot spec with default or specified axis sharing parameters."""
        pass

    def init_figure(self, pair_spec: PairSpec, pyplot: bool=False, figure_kws: dict | None=None, target: Axes | Figure | SubFigure | None=None) -> Figure:
        """Initialize matplotlib objects and add seaborn-relevant metadata."""
        pass

    def __iter__(self) -> Generator[dict, None, None]:
        """Yield each subplot dictionary with Axes object and metadata."""
        yield from self._subplot_list

    def __len__(self) -> int:
        """Return the number of subplots in this figure."""
        return len(self._subplot_list)