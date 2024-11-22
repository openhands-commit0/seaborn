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

def groupby_apply_include_groups(df, grouper, func, *args, **kwargs):
    """Apply a function to each group in a DataFrame, including empty groups.
    
    This function ensures that empty groups are included in the result, which is
    important for maintaining consistent behavior across different pandas versions.
    """
    # Get all unique values in the grouper
    if isinstance(grouper, str):
        unique_groups = df[grouper].unique()
    else:
        unique_groups = pd.Series(grouper).unique()
    
    # Apply the function to each group
    result = df.groupby(grouper, observed=True).apply(func, *args, **kwargs)
    
    # If result is empty or doesn't include all groups, handle empty groups
    if len(result) < len(unique_groups):
        empty_groups = set(unique_groups) - set(result.index)
        for group in empty_groups:
            empty_df = df.iloc[0:0].copy()  # Empty DataFrame with same structure
            empty_result = func(empty_df, *args, **kwargs)
            if isinstance(result, pd.Series):
                result[group] = empty_result
            else:
                result.loc[group] = empty_result
    
    return result