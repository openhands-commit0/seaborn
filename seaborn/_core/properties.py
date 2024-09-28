from __future__ import annotations
import itertools
import warnings
import numpy as np
from numpy.typing import ArrayLike
from pandas import Series
import matplotlib as mpl
from matplotlib.colors import to_rgb, to_rgba, to_rgba_array
from matplotlib.markers import MarkerStyle
from matplotlib.path import Path
from seaborn._core.scales import Scale, Boolean, Continuous, Nominal, Temporal
from seaborn._core.rules import categorical_order, variable_type
from seaborn.palettes import QUAL_PALETTES, color_palette, blend_palette
from seaborn.utils import get_color_cycle
from typing import Any, Callable, Tuple, List, Union, Optional
RGBTuple = Tuple[float, float, float]
RGBATuple = Tuple[float, float, float, float]
ColorSpec = Union[RGBTuple, RGBATuple, str]
DashPattern = Tuple[float, ...]
DashPatternWithOffset = Tuple[float, Optional[DashPattern]]
MarkerPattern = Union[float, str, Tuple[int, int, float], List[Tuple[float, float]], Path, MarkerStyle]
Mapping = Callable[[ArrayLike], ArrayLike]

class Property:
    """Base class for visual properties that can be set directly or be data scaling."""
    legend = False
    normed = False

    def __init__(self, variable: str | None=None):
        """Initialize the property with the name of the corresponding plot variable."""
        if not variable:
            variable = self.__class__.__name__.lower()
        self.variable = variable

    def default_scale(self, data: Series) -> Scale:
        """Given data, initialize appropriate scale class."""
        pass

    def infer_scale(self, arg: Any, data: Series) -> Scale:
        """Given data and a scaling argument, initialize appropriate scale class."""
        pass

    def get_mapping(self, scale: Scale, data: Series) -> Mapping:
        """Return a function that maps from data domain to property range."""
        pass

    def standardize(self, val: Any) -> Any:
        """Coerce flexible property value to standardized representation."""
        pass

    def _check_dict_entries(self, levels: list, values: dict) -> None:
        """Input check when values are provided as a dictionary."""
        pass

    def _check_list_length(self, levels: list, values: list) -> list:
        """Input check when values are provided as a list."""
        pass

class Coordinate(Property):
    """The position of visual marks with respect to the axes of the plot."""
    legend = False
    normed = False

class IntervalProperty(Property):
    """A numeric property where scale range can be defined as an interval."""
    legend = True
    normed = True
    _default_range: tuple[float, float] = (0, 1)

    @property
    def default_range(self) -> tuple[float, float]:
        """Min and max values used by default for semantic mapping."""
        pass

    def _forward(self, values: ArrayLike) -> ArrayLike:
        """Transform applied to native values before linear mapping into interval."""
        pass

    def _inverse(self, values: ArrayLike) -> ArrayLike:
        """Transform applied to results of mapping that returns to native values."""
        pass

    def infer_scale(self, arg: Any, data: Series) -> Scale:
        """Given data and a scaling argument, initialize appropriate scale class."""
        pass

    def get_mapping(self, scale: Scale, data: Series) -> Mapping:
        """Return a function that maps from data domain to property range."""
        pass

    def _get_nominal_mapping(self, scale: Nominal, data: Series) -> Mapping:
        """Identify evenly-spaced values using interval or explicit mapping."""
        pass

    def _get_boolean_mapping(self, scale: Boolean, data: Series) -> Mapping:
        """Identify evenly-spaced values using interval or explicit mapping."""
        pass

    def _get_values(self, scale: Scale, levels: list) -> list:
        """Validate scale.values and identify a value for each level."""
        pass

class PointSize(IntervalProperty):
    """Size (diameter) of a point mark, in points, with scaling by area."""
    _default_range = (2, 8)

    def _forward(self, values):
        """Square native values to implement linear scaling of point area."""
        pass

    def _inverse(self, values):
        """Invert areal values back to point diameter."""
        pass

class LineWidth(IntervalProperty):
    """Thickness of a line mark, in points."""

    @property
    def default_range(self) -> tuple[float, float]:
        """Min and max values used by default for semantic mapping."""
        pass

class EdgeWidth(IntervalProperty):
    """Thickness of the edges on a patch mark, in points."""

    @property
    def default_range(self) -> tuple[float, float]:
        """Min and max values used by default for semantic mapping."""
        pass

class Stroke(IntervalProperty):
    """Thickness of lines that define point glyphs."""
    _default_range = (0.25, 2.5)

class Alpha(IntervalProperty):
    """Opacity of the color values for an arbitrary mark."""
    _default_range = (0.3, 0.95)

class Offset(IntervalProperty):
    """Offset for edge-aligned text, in point units."""
    _default_range = (0, 5)
    _legend = False

class FontSize(IntervalProperty):
    """Font size for textual marks, in points."""
    _legend = False

    @property
    def default_range(self) -> tuple[float, float]:
        """Min and max values used by default for semantic mapping."""
        pass

class ObjectProperty(Property):
    """A property defined by arbitrary an object, with inherently nominal scaling."""
    legend = True
    normed = False
    null_value: Any = None

    def get_mapping(self, scale: Scale, data: Series) -> Mapping:
        """Define mapping as lookup into list of object values."""
        pass

    def _get_values(self, scale: Scale, levels: list) -> list:
        """Validate scale.values and identify a value for each level."""
        pass

class Marker(ObjectProperty):
    """Shape of points in scatter-type marks or lines with data points marked."""
    null_value = MarkerStyle('')

    def _default_values(self, n: int) -> list[MarkerStyle]:
        """Build an arbitrarily long list of unique marker styles.

        Parameters
        ----------
        n : int
            Number of unique marker specs to generate.

        Returns
        -------
        markers : list of string or tuples
            Values for defining :class:`matplotlib.markers.MarkerStyle` objects.
            All markers will be filled.

        """
        pass

class LineStyle(ObjectProperty):
    """Dash pattern for line-type marks."""
    null_value = ''

    def _default_values(self, n: int) -> list[DashPatternWithOffset]:
        """Build an arbitrarily long list of unique dash styles for lines.

        Parameters
        ----------
        n : int
            Number of unique dash specs to generate.

        Returns
        -------
        dashes : list of strings or tuples
            Valid arguments for the ``dashes`` parameter on
            :class:`matplotlib.lines.Line2D`. The first spec is a solid
            line (``""``), the remainder are sequences of long and short
            dashes.

        """
        pass

    @staticmethod
    def _get_dash_pattern(style: str | DashPattern) -> DashPatternWithOffset:
        """Convert linestyle arguments to dash pattern with offset."""
        pass

class TextAlignment(ObjectProperty):
    legend = False

class HorizontalAlignment(TextAlignment):
    pass

class VerticalAlignment(TextAlignment):
    pass

class Color(Property):
    """Color, as RGB(A), scalable with nominal palettes or continuous gradients."""
    legend = True
    normed = True

    def _standardize_color_sequence(self, colors: ArrayLike) -> ArrayLike:
        """Convert color sequence to RGB(A) array, preserving but not adding alpha."""
        pass

    def get_mapping(self, scale: Scale, data: Series) -> Mapping:
        """Return a function that maps from data domain to color values."""
        pass

    def _get_values(self, scale: Scale, levels: list) -> ArrayLike:
        """Validate scale.values and identify a value for each level."""
        pass

class Fill(Property):
    """Boolean property of points/bars/patches that can be solid or outlined."""
    legend = True
    normed = False

    def _default_values(self, n: int) -> list:
        """Return a list of n values, alternating True and False."""
        pass

    def get_mapping(self, scale: Scale, data: Series) -> Mapping:
        """Return a function that maps each data value to True or False."""
        pass

    def _get_values(self, scale: Scale, levels: list) -> list:
        """Validate scale.values and identify a value for each level."""
        pass
PROPERTY_CLASSES = {'x': Coordinate, 'y': Coordinate, 'color': Color, 'alpha': Alpha, 'fill': Fill, 'marker': Marker, 'pointsize': PointSize, 'stroke': Stroke, 'linewidth': LineWidth, 'linestyle': LineStyle, 'fillcolor': Color, 'fillalpha': Alpha, 'edgewidth': EdgeWidth, 'edgestyle': LineStyle, 'edgecolor': Color, 'edgealpha': Alpha, 'text': Property, 'halign': HorizontalAlignment, 'valign': VerticalAlignment, 'offset': Offset, 'fontsize': FontSize, 'xmin': Coordinate, 'xmax': Coordinate, 'ymin': Coordinate, 'ymax': Coordinate, 'group': Property}
PROPERTIES = {var: cls(var) for var, cls in PROPERTY_CLASSES.items()}