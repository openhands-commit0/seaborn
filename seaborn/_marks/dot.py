from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import matplotlib as mpl
from seaborn._marks.base import Mark, Mappable, MappableBool, MappableFloat, MappableString, MappableColor, MappableStyle, resolve_properties, resolve_color, document_properties
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any
    from matplotlib.artist import Artist
    from seaborn._core.scales import Scale

class DotBase(Mark):
    pass

@document_properties
@dataclass
class Dot(DotBase):
    """
    A mark suitable for dot plots or less-dense scatterplots.

    See also
    --------
    Dots : A dot mark defined by strokes to better handle overplotting.

    Examples
    --------
    .. include:: ../docstrings/objects.Dot.rst

    """
    marker: MappableString = Mappable('o', grouping=False)
    pointsize: MappableFloat = Mappable(6, grouping=False)
    stroke: MappableFloat = Mappable(0.75, grouping=False)
    color: MappableColor = Mappable('C0', grouping=False)
    alpha: MappableFloat = Mappable(1, grouping=False)
    fill: MappableBool = Mappable(True, grouping=False)
    edgecolor: MappableColor = Mappable(depend='color', grouping=False)
    edgealpha: MappableFloat = Mappable(depend='alpha', grouping=False)
    edgewidth: MappableFloat = Mappable(0.5, grouping=False)
    edgestyle: MappableStyle = Mappable('-', grouping=False)

@document_properties
@dataclass
class Dots(DotBase):
    """
    A dot mark defined by strokes to better handle overplotting.

    See also
    --------
    Dot : A mark suitable for dot plots or less-dense scatterplots.

    Examples
    --------
    .. include:: ../docstrings/objects.Dots.rst

    """
    marker: MappableString = Mappable(rc='scatter.marker', grouping=False)
    pointsize: MappableFloat = Mappable(4, grouping=False)
    stroke: MappableFloat = Mappable(0.75, grouping=False)
    color: MappableColor = Mappable('C0', grouping=False)
    alpha: MappableFloat = Mappable(1, grouping=False)
    fill: MappableBool = Mappable(True, grouping=False)
    fillcolor: MappableColor = Mappable(depend='color', grouping=False)
    fillalpha: MappableFloat = Mappable(0.2, grouping=False)