from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
import numpy as np
import matplotlib as mpl
from matplotlib.transforms import ScaledTranslation
from seaborn._marks.base import Mark, Mappable, MappableFloat, MappableString, MappableColor, resolve_properties, resolve_color, document_properties

@document_properties
@dataclass
class Text(Mark):
    """
    A textual mark to annotate or represent data values.

    Examples
    --------
    .. include:: ../docstrings/objects.Text.rst

    """
    text: MappableString = Mappable('')
    color: MappableColor = Mappable('k')
    alpha: MappableFloat = Mappable(1)
    fontsize: MappableFloat = Mappable(rc='font.size')
    halign: MappableString = Mappable('center')
    valign: MappableString = Mappable('center_baseline')
    offset: MappableFloat = Mappable(4)