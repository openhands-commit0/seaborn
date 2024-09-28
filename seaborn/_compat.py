from __future__ import annotations
from typing import Literal
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib.figure import Figure
from seaborn.utils import _version_predates

def norm_from_scale(scale, norm):
    """Produce a Normalize object given a Scale and min/max domain limits."""
    pass

def get_colormap(name):
    """Handle changes to matplotlib colormap interface in 3.6."""
    pass

def register_colormap(name, cmap):
    """Handle changes to matplotlib colormap interface in 3.6."""
    pass

def set_layout_engine(fig: Figure, engine: Literal['constrained', 'compressed', 'tight', 'none']) -> None:
    """Handle changes to auto layout engine interface in 3.6"""
    pass

def get_layout_engine(fig: Figure) -> mpl.layout_engine.LayoutEngine | None:
    """Handle changes to auto layout engine interface in 3.6"""
    pass

def share_axis(ax0, ax1, which):
    """Handle changes to post-hoc axis sharing."""
    pass

def get_legend_handles(legend):
    """Handle legendHandles attribute rename."""
    pass