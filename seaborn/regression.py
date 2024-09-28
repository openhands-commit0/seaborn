"""Plotting functions for linear models (broadly construed)."""
import copy
from textwrap import dedent
import warnings
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
try:
    import statsmodels
    assert statsmodels
    _has_statsmodels = True
except ImportError:
    _has_statsmodels = False
from . import utils
from . import algorithms as algo
from .axisgrid import FacetGrid, _facet_docs
__all__ = ['lmplot', 'regplot', 'residplot']

class _LinearPlotter:
    """Base class for plotting relational data in tidy format.

    To get anything useful done you'll have to inherit from this, but setup
    code that can be abstracted out should be put here.

    """

    def establish_variables(self, data, **kws):
        """Extract variables from data or use directly."""
        pass

    def dropna(self, *vars):
        """Remove observations with missing data."""
        pass

class _RegressionPlotter(_LinearPlotter):
    """Plotter for numeric independent variables with regression model.

    This does the computations and drawing for the `regplot` function, and
    is thus also used indirectly by `lmplot`.
    """

    def __init__(self, x, y, data=None, x_estimator=None, x_bins=None, x_ci='ci', scatter=True, fit_reg=True, ci=95, n_boot=1000, units=None, seed=None, order=1, logistic=False, lowess=False, robust=False, logx=False, x_partial=None, y_partial=None, truncate=False, dropna=True, x_jitter=None, y_jitter=None, color=None, label=None):
        self.x_estimator = x_estimator
        self.ci = ci
        self.x_ci = ci if x_ci == 'ci' else x_ci
        self.n_boot = n_boot
        self.seed = seed
        self.scatter = scatter
        self.fit_reg = fit_reg
        self.order = order
        self.logistic = logistic
        self.lowess = lowess
        self.robust = robust
        self.logx = logx
        self.truncate = truncate
        self.x_jitter = x_jitter
        self.y_jitter = y_jitter
        self.color = color
        self.label = label
        if sum((order > 1, logistic, robust, lowess, logx)) > 1:
            raise ValueError('Mutually exclusive regression options.')
        self.establish_variables(data, x=x, y=y, units=units, x_partial=x_partial, y_partial=y_partial)
        if dropna:
            self.dropna('x', 'y', 'units', 'x_partial', 'y_partial')
        if self.x_partial is not None:
            self.x = self.regress_out(self.x, self.x_partial)
        if self.y_partial is not None:
            self.y = self.regress_out(self.y, self.y_partial)
        if x_bins is not None:
            self.x_estimator = np.mean if x_estimator is None else x_estimator
            x_discrete, x_bins = self.bin_predictor(x_bins)
            self.x_discrete = x_discrete
        else:
            self.x_discrete = self.x
        if len(self.x) <= 1:
            self.fit_reg = False
        if self.fit_reg:
            self.x_range = (self.x.min(), self.x.max())

    @property
    def scatter_data(self):
        """Data where each observation is a point."""
        pass

    @property
    def estimate_data(self):
        """Data with a point estimate and CI for each discrete x value."""
        pass

    def _check_statsmodels(self):
        """Check whether statsmodels is installed if any boolean options require it."""
        pass

    def fit_regression(self, ax=None, x_range=None, grid=None):
        """Fit the regression model."""
        pass

    def fit_fast(self, grid):
        """Low-level regression and prediction using linear algebra."""
        pass

    def fit_poly(self, grid, order):
        """Regression using numpy polyfit for higher-order trends."""
        pass

    def fit_statsmodels(self, grid, model, **kwargs):
        """More general regression function using statsmodels objects."""
        pass

    def fit_lowess(self):
        """Fit a locally-weighted regression, which returns its own grid."""
        pass

    def fit_logx(self, grid):
        """Fit the model in log-space."""
        pass

    def bin_predictor(self, bins):
        """Discretize a predictor by assigning value to closest bin."""
        pass

    def regress_out(self, a, b):
        """Regress b from a keeping a's original mean."""
        pass

    def plot(self, ax, scatter_kws, line_kws):
        """Draw the full plot."""
        pass

    def scatterplot(self, ax, kws):
        """Draw the data."""
        pass

    def lineplot(self, ax, kws):
        """Draw the model."""
        pass
_regression_docs = dict(model_api=dedent('    There are a number of mutually exclusive options for estimating the\n    regression model. See the :ref:`tutorial <regression_tutorial>` for more\n    information.    '), regplot_vs_lmplot=dedent('    The :func:`regplot` and :func:`lmplot` functions are closely related, but\n    the former is an axes-level function while the latter is a figure-level\n    function that combines :func:`regplot` and :class:`FacetGrid`.    '), x_estimator=dedent('    x_estimator : callable that maps vector -> scalar, optional\n        Apply this function to each unique value of ``x`` and plot the\n        resulting estimate. This is useful when ``x`` is a discrete variable.\n        If ``x_ci`` is given, this estimate will be bootstrapped and a\n        confidence interval will be drawn.    '), x_bins=dedent('    x_bins : int or vector, optional\n        Bin the ``x`` variable into discrete bins and then estimate the central\n        tendency and a confidence interval. This binning only influences how\n        the scatterplot is drawn; the regression is still fit to the original\n        data.  This parameter is interpreted either as the number of\n        evenly-sized (not necessary spaced) bins or the positions of the bin\n        centers. When this parameter is used, it implies that the default of\n        ``x_estimator`` is ``numpy.mean``.    '), x_ci=dedent('    x_ci : "ci", "sd", int in [0, 100] or None, optional\n        Size of the confidence interval used when plotting a central tendency\n        for discrete values of ``x``. If ``"ci"``, defer to the value of the\n        ``ci`` parameter. If ``"sd"``, skip bootstrapping and show the\n        standard deviation of the observations in each bin.    '), scatter=dedent('    scatter : bool, optional\n        If ``True``, draw a scatterplot with the underlying observations (or\n        the ``x_estimator`` values).    '), fit_reg=dedent('    fit_reg : bool, optional\n        If ``True``, estimate and plot a regression model relating the ``x``\n        and ``y`` variables.    '), ci=dedent('    ci : int in [0, 100] or None, optional\n        Size of the confidence interval for the regression estimate. This will\n        be drawn using translucent bands around the regression line. The\n        confidence interval is estimated using a bootstrap; for large\n        datasets, it may be advisable to avoid that computation by setting\n        this parameter to None.    '), n_boot=dedent('    n_boot : int, optional\n        Number of bootstrap resamples used to estimate the ``ci``. The default\n        value attempts to balance time and stability; you may want to increase\n        this value for "final" versions of plots.    '), units=dedent('    units : variable name in ``data``, optional\n        If the ``x`` and ``y`` observations are nested within sampling units,\n        those can be specified here. This will be taken into account when\n        computing the confidence intervals by performing a multilevel bootstrap\n        that resamples both units and observations (within unit). This does not\n        otherwise influence how the regression is estimated or drawn.    '), seed=dedent('    seed : int, numpy.random.Generator, or numpy.random.RandomState, optional\n        Seed or random number generator for reproducible bootstrapping.    '), order=dedent('    order : int, optional\n        If ``order`` is greater than 1, use ``numpy.polyfit`` to estimate a\n        polynomial regression.    '), logistic=dedent('    logistic : bool, optional\n        If ``True``, assume that ``y`` is a binary variable and use\n        ``statsmodels`` to estimate a logistic regression model. Note that this\n        is substantially more computationally intensive than linear regression,\n        so you may wish to decrease the number of bootstrap resamples\n        (``n_boot``) or set ``ci`` to None.    '), lowess=dedent('    lowess : bool, optional\n        If ``True``, use ``statsmodels`` to estimate a nonparametric lowess\n        model (locally weighted linear regression). Note that confidence\n        intervals cannot currently be drawn for this kind of model.    '), robust=dedent('    robust : bool, optional\n        If ``True``, use ``statsmodels`` to estimate a robust regression. This\n        will de-weight outliers. Note that this is substantially more\n        computationally intensive than standard linear regression, so you may\n        wish to decrease the number of bootstrap resamples (``n_boot``) or set\n        ``ci`` to None.    '), logx=dedent('    logx : bool, optional\n        If ``True``, estimate a linear regression of the form y ~ log(x), but\n        plot the scatterplot and regression model in the input space. Note that\n        ``x`` must be positive for this to work.    '), xy_partial=dedent('    {x,y}_partial : strings in ``data`` or matrices\n        Confounding variables to regress out of the ``x`` or ``y`` variables\n        before plotting.    '), truncate=dedent('    truncate : bool, optional\n        If ``True``, the regression line is bounded by the data limits. If\n        ``False``, it extends to the ``x`` axis limits.\n    '), xy_jitter=dedent('    {x,y}_jitter : floats, optional\n        Add uniform random noise of this size to either the ``x`` or ``y``\n        variables. The noise is added to a copy of the data after fitting the\n        regression, and only influences the look of the scatterplot. This can\n        be helpful when plotting variables that take discrete values.    '), scatter_line_kws=dedent('    {scatter,line}_kws : dictionaries\n        Additional keyword arguments to pass to ``plt.scatter`` and\n        ``plt.plot``.    '))
_regression_docs.update(_facet_docs)
lmplot.__doc__ = dedent('    Plot data and regression model fits across a FacetGrid.\n\n    This function combines :func:`regplot` and :class:`FacetGrid`. It is\n    intended as a convenient interface to fit regression models across\n    conditional subsets of a dataset.\n\n    When thinking about how to assign variables to different facets, a general\n    rule is that it makes sense to use ``hue`` for the most important\n    comparison, followed by ``col`` and ``row``. However, always think about\n    your particular dataset and the goals of the visualization you are\n    creating.\n\n    {model_api}\n\n    The parameters to this function span most of the options in\n    :class:`FacetGrid`, although there may be occasional cases where you will\n    want to use that class and :func:`regplot` directly.\n\n    Parameters\n    ----------\n    {data}\n    x, y : strings, optional\n        Input variables; these should be column names in ``data``.\n    hue, col, row : strings\n        Variables that define subsets of the data, which will be drawn on\n        separate facets in the grid. See the ``*_order`` parameters to control\n        the order of levels of this variable.\n    {palette}\n    {col_wrap}\n    {height}\n    {aspect}\n    markers : matplotlib marker code or list of marker codes, optional\n        Markers for the scatterplot. If a list, each marker in the list will be\n        used for each level of the ``hue`` variable.\n    {share_xy}\n\n        .. deprecated:: 0.12.0\n            Pass using the `facet_kws` dictionary.\n\n    {{hue,col,row}}_order : lists, optional\n        Order for the levels of the faceting variables. By default, this will\n        be the order that the levels appear in ``data`` or, if the variables\n        are pandas categoricals, the category order.\n    legend : bool, optional\n        If ``True`` and there is a ``hue`` variable, add a legend.\n    {legend_out}\n\n        .. deprecated:: 0.12.0\n            Pass using the `facet_kws` dictionary.\n\n    {x_estimator}\n    {x_bins}\n    {x_ci}\n    {scatter}\n    {fit_reg}\n    {ci}\n    {n_boot}\n    {units}\n    {seed}\n    {order}\n    {logistic}\n    {lowess}\n    {robust}\n    {logx}\n    {xy_partial}\n    {truncate}\n    {xy_jitter}\n    {scatter_line_kws}\n    facet_kws : dict\n        Dictionary of keyword arguments for :class:`FacetGrid`.\n\n    See Also\n    --------\n    regplot : Plot data and a conditional model fit.\n    FacetGrid : Subplot grid for plotting conditional relationships.\n    pairplot : Combine :func:`regplot` and :class:`PairGrid` (when used with\n               ``kind="reg"``).\n\n    Notes\n    -----\n\n    {regplot_vs_lmplot}\n\n    Examples\n    --------\n\n    .. include:: ../docstrings/lmplot.rst\n\n    ').format(**_regression_docs)
regplot.__doc__ = dedent('    Plot data and a linear regression model fit.\n\n    {model_api}\n\n    Parameters\n    ----------\n    x, y: string, series, or vector array\n        Input variables. If strings, these should correspond with column names\n        in ``data``. When pandas objects are used, axes will be labeled with\n        the series name.\n    {data}\n    {x_estimator}\n    {x_bins}\n    {x_ci}\n    {scatter}\n    {fit_reg}\n    {ci}\n    {n_boot}\n    {units}\n    {seed}\n    {order}\n    {logistic}\n    {lowess}\n    {robust}\n    {logx}\n    {xy_partial}\n    {truncate}\n    {xy_jitter}\n    label : string\n        Label to apply to either the scatterplot or regression line (if\n        ``scatter`` is ``False``) for use in a legend.\n    color : matplotlib color\n        Color to apply to all plot elements; will be superseded by colors\n        passed in ``scatter_kws`` or ``line_kws``.\n    marker : matplotlib marker code\n        Marker to use for the scatterplot glyphs.\n    {scatter_line_kws}\n    ax : matplotlib Axes, optional\n        Axes object to draw the plot onto, otherwise uses the current Axes.\n\n    Returns\n    -------\n    ax : matplotlib Axes\n        The Axes object containing the plot.\n\n    See Also\n    --------\n    lmplot : Combine :func:`regplot` and :class:`FacetGrid` to plot multiple\n             linear relationships in a dataset.\n    jointplot : Combine :func:`regplot` and :class:`JointGrid` (when used with\n                ``kind="reg"``).\n    pairplot : Combine :func:`regplot` and :class:`PairGrid` (when used with\n               ``kind="reg"``).\n    residplot : Plot the residuals of a linear regression model.\n\n    Notes\n    -----\n\n    {regplot_vs_lmplot}\n\n\n    It\'s also easy to combine :func:`regplot` and :class:`JointGrid` or\n    :class:`PairGrid` through the :func:`jointplot` and :func:`pairplot`\n    functions, although these do not directly accept all of :func:`regplot`\'s\n    parameters.\n\n    Examples\n    --------\n\n    .. include:: ../docstrings/regplot.rst\n\n    ').format(**_regression_docs)

def residplot(data=None, *, x=None, y=None, x_partial=None, y_partial=None, lowess=False, order=1, robust=False, dropna=True, label=None, color=None, scatter_kws=None, line_kws=None, ax=None):
    """Plot the residuals of a linear regression.

    This function will regress y on x (possibly as a robust or polynomial
    regression) and then draw a scatterplot of the residuals. You can
    optionally fit a lowess smoother to the residual plot, which can
    help in determining if there is structure to the residuals.

    Parameters
    ----------
    data : DataFrame, optional
        DataFrame to use if `x` and `y` are column names.
    x : vector or string
        Data or column name in `data` for the predictor variable.
    y : vector or string
        Data or column name in `data` for the response variable.
    {x, y}_partial : vectors or string(s) , optional
        These variables are treated as confounding and are removed from
        the `x` or `y` variables before plotting.
    lowess : boolean, optional
        Fit a lowess smoother to the residual scatterplot.
    order : int, optional
        Order of the polynomial to fit when calculating the residuals.
    robust : boolean, optional
        Fit a robust linear regression when calculating the residuals.
    dropna : boolean, optional
        If True, ignore observations with missing data when fitting and
        plotting.
    label : string, optional
        Label that will be used in any plot legends.
    color : matplotlib color, optional
        Color to use for all elements of the plot.
    {scatter, line}_kws : dictionaries, optional
        Additional keyword arguments passed to scatter() and plot() for drawing
        the components of the plot.
    ax : matplotlib axis, optional
        Plot into this axis, otherwise grab the current axis or make a new
        one if not existing.

    Returns
    -------
    ax: matplotlib axes
        Axes with the regression plot.

    See Also
    --------
    regplot : Plot a simple linear regression model.
    jointplot : Draw a :func:`residplot` with univariate marginal distributions
                (when used with ``kind="resid"``).

    Examples
    --------

    .. include:: ../docstrings/residplot.rst

    """
    pass