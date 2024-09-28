from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
import numpy as np
import matplotlib as mpl
from seaborn._marks.base import Mark, Mappable, MappableBool, MappableColor, MappableFloat, MappableStyle, resolve_properties, resolve_color, document_properties
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any
    from matplotlib.artist import Artist
    from seaborn._core.scales import Scale

class BarBase(Mark):
    pass

@document_properties
@dataclass
class Bar(BarBase):
    """
    A bar mark drawn between baseline and data values.

    See also
    --------
    Bars : A faster bar mark with defaults more suitable for histograms.

    Examples
    --------
    .. include:: ../docstrings/objects.Bar.rst

    """
    color: MappableColor = Mappable('C0', grouping=False)
    alpha: MappableFloat = Mappable(0.7, grouping=False)
    fill: MappableBool = Mappable(True, grouping=False)
    edgecolor: MappableColor = Mappable(depend='color', grouping=False)
    edgealpha: MappableFloat = Mappable(1, grouping=False)
    edgewidth: MappableFloat = Mappable(rc='patch.linewidth', grouping=False)
    edgestyle: MappableStyle = Mappable('-', grouping=False)
    width: MappableFloat = Mappable(0.8, grouping=False)
    baseline: MappableFloat = Mappable(0, grouping=False)

@document_properties
@dataclass
class Bars(BarBase):
    """
    A faster bar mark with defaults more suitable for histograms.

    See also
    --------
    Bar : A bar mark drawn between baseline and data values.

    Examples
    --------
    .. include:: ../docstrings/objects.Bars.rst

    """
    color: MappableColor = Mappable('C0', grouping=False)
    alpha: MappableFloat = Mappable(0.7, grouping=False)
    fill: MappableBool = Mappable(True, grouping=False)
    edgecolor: MappableColor = Mappable(rc='patch.edgecolor', grouping=False)
    edgealpha: MappableFloat = Mappable(1, grouping=False)
    edgewidth: MappableFloat = Mappable(auto=True, grouping=False)
    edgestyle: MappableStyle = Mappable('-', grouping=False)
    width: MappableFloat = Mappable(1, grouping=False)
    baseline: MappableFloat = Mappable(0, grouping=False)