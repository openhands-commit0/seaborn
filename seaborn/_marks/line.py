from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
import numpy as np
import matplotlib as mpl
from seaborn._marks.base import Mark, Mappable, MappableFloat, MappableString, MappableColor, resolve_properties, resolve_color, document_properties

@document_properties
@dataclass
class Path(Mark):
    """
    A mark connecting data points in the order they appear.

    See also
    --------
    Line : A mark connecting data points with sorting along the orientation axis.
    Paths : A faster but less-flexible mark for drawing many paths.

    Examples
    --------
    .. include:: ../docstrings/objects.Path.rst

    """
    color: MappableColor = Mappable('C0')
    alpha: MappableFloat = Mappable(1)
    linewidth: MappableFloat = Mappable(rc='lines.linewidth')
    linestyle: MappableString = Mappable(rc='lines.linestyle')
    marker: MappableString = Mappable(rc='lines.marker')
    pointsize: MappableFloat = Mappable(rc='lines.markersize')
    fillcolor: MappableColor = Mappable(depend='color')
    edgecolor: MappableColor = Mappable(depend='color')
    edgewidth: MappableFloat = Mappable(rc='lines.markeredgewidth')
    _sort: ClassVar[bool] = False

@document_properties
@dataclass
class Line(Path):
    """
    A mark connecting data points with sorting along the orientation axis.

    See also
    --------
    Path : A mark connecting data points in the order they appear.
    Lines : A faster but less-flexible mark for drawing many lines.

    Examples
    --------
    .. include:: ../docstrings/objects.Line.rst

    """
    _sort: ClassVar[bool] = True

@document_properties
@dataclass
class Paths(Mark):
    """
    A faster but less-flexible mark for drawing many paths.

    See also
    --------
    Path : A mark connecting data points in the order they appear.

    Examples
    --------
    .. include:: ../docstrings/objects.Paths.rst

    """
    color: MappableColor = Mappable('C0')
    alpha: MappableFloat = Mappable(1)
    linewidth: MappableFloat = Mappable(rc='lines.linewidth')
    linestyle: MappableString = Mappable(rc='lines.linestyle')
    _sort: ClassVar[bool] = False

    def __post_init__(self):
        self.artist_kws.setdefault('capstyle', mpl.rcParams['lines.solid_capstyle'])

@document_properties
@dataclass
class Lines(Paths):
    """
    A faster but less-flexible mark for drawing many lines.

    See also
    --------
    Line : A mark connecting data points with sorting along the orientation axis.

    Examples
    --------
    .. include:: ../docstrings/objects.Lines.rst

    """
    _sort: ClassVar[bool] = True

@document_properties
@dataclass
class Range(Paths):
    """
    An oriented line mark drawn between min/max values.

    Examples
    --------
    .. include:: ../docstrings/objects.Range.rst

    """

@document_properties
@dataclass
class Dash(Paths):
    """
    A line mark drawn as an oriented segment for each datapoint.

    Examples
    --------
    .. include:: ../docstrings/objects.Dash.rst

    """
    width: MappableFloat = Mappable(0.8, grouping=False)