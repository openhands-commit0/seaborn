from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
import numpy as np
import matplotlib as mpl
from seaborn._marks.base import Mark, Mappable, MappableBool, MappableFloat, MappableColor, MappableStyle, resolve_properties, resolve_color, document_properties

class AreaBase:
    pass

@document_properties
@dataclass
class Area(AreaBase, Mark):
    """
    A fill mark drawn from a baseline to data values.

    See also
    --------
    Band : A fill mark representing an interval between values.

    Examples
    --------
    .. include:: ../docstrings/objects.Area.rst

    """
    color: MappableColor = Mappable('C0')
    alpha: MappableFloat = Mappable(0.2)
    fill: MappableBool = Mappable(True)
    edgecolor: MappableColor = Mappable(depend='color')
    edgealpha: MappableFloat = Mappable(1)
    edgewidth: MappableFloat = Mappable(rc='patch.linewidth')
    edgestyle: MappableStyle = Mappable('-')
    baseline: MappableFloat = Mappable(0, grouping=False)

@document_properties
@dataclass
class Band(AreaBase, Mark):
    """
    A fill mark representing an interval between values.

    See also
    --------
    Area : A fill mark drawn from a baseline to data values.

    Examples
    --------
    .. include:: ../docstrings/objects.Band.rst

    """
    color: MappableColor = Mappable('C0')
    alpha: MappableFloat = Mappable(0.2)
    fill: MappableBool = Mappable(True)
    edgecolor: MappableColor = Mappable(depend='color')
    edgealpha: MappableFloat = Mappable(1)
    edgewidth: MappableFloat = Mappable(0)
    edgestyle: MappableFloat = Mappable('-')