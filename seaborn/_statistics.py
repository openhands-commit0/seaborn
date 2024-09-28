"""Statistical transformations for visualization.

This module is currently private, but is being written to eventually form part
of the public API.

The classes should behave roughly in the style of scikit-learn.

- All data-independent parameters should be passed to the class constructor.
- Each class should implement a default transformation that is exposed through
  __call__. These are currently written for vector arguments, but I think
  consuming a whole `plot_data` DataFrame and return it with transformed
  variables would make more sense.
- Some class have data-dependent preprocessing that should be cached and used
  multiple times (think defining histogram bins off all data and then counting
  observations within each bin multiple times per data subsets). These currently
  have unique names, but it would be good to have a common name. Not quite
  `fit`, but something similar.
- Alternatively, the transform interface could take some information about grouping
  variables and do a groupby internally.
- Some classes should define alternate transforms that might make the most sense
  with a different function. For example, KDE usually evaluates the distribution
  on a regular grid, but it would be useful for it to transform at the actual
  datapoints. Then again, this could be controlled by a parameter at  the time of
  class instantiation.

"""
from numbers import Number
from statistics import NormalDist
import numpy as np
import pandas as pd
try:
    from scipy.stats import gaussian_kde
    _no_scipy = False
except ImportError:
    from .external.kde import gaussian_kde
    _no_scipy = True
from .algorithms import bootstrap
from .utils import _check_argument

class KDE:
    """Univariate and bivariate kernel density estimator."""

    def __init__(self, *, bw_method=None, bw_adjust=1, gridsize=200, cut=3, clip=None, cumulative=False):
        """Initialize the estimator with its parameters.

        Parameters
        ----------
        bw_method : string, scalar, or callable, optional
            Method for determining the smoothing bandwidth to use; passed to
            :class:`scipy.stats.gaussian_kde`.
        bw_adjust : number, optional
            Factor that multiplicatively scales the value chosen using
            ``bw_method``. Increasing will make the curve smoother. See Notes.
        gridsize : int, optional
            Number of points on each dimension of the evaluation grid.
        cut : number, optional
            Factor, multiplied by the smoothing bandwidth, that determines how
            far the evaluation grid extends past the extreme datapoints. When
            set to 0, truncate the curve at the data limits.
        clip : pair of numbers or None, or a pair of such pairs
            Do not evaluate the density outside of these limits.
        cumulative : bool, optional
            If True, estimate a cumulative distribution function. Requires scipy.

        """
        if clip is None:
            clip = (None, None)
        self.bw_method = bw_method
        self.bw_adjust = bw_adjust
        self.gridsize = gridsize
        self.cut = cut
        self.clip = clip
        self.cumulative = cumulative
        if cumulative and _no_scipy:
            raise RuntimeError('Cumulative KDE evaluation requires scipy')
        self.support = None

    def _define_support_grid(self, x, bw, cut, clip, gridsize):
        """Create the grid of evaluation points depending for vector x."""
        pass

    def _define_support_univariate(self, x, weights):
        """Create a 1D grid of evaluation points."""
        pass

    def _define_support_bivariate(self, x1, x2, weights):
        """Create a 2D grid of evaluation points."""
        pass

    def define_support(self, x1, x2=None, weights=None, cache=True):
        """Create the evaluation grid for a given data set."""
        pass

    def _fit(self, fit_data, weights=None):
        """Fit the scipy kde while adding bw_adjust logic and version check."""
        pass

    def _eval_univariate(self, x, weights=None):
        """Fit and evaluate a univariate on univariate data."""
        pass

    def _eval_bivariate(self, x1, x2, weights=None):
        """Fit and evaluate a univariate on bivariate data."""
        pass

    def __call__(self, x1, x2=None, weights=None):
        """Fit and evaluate on univariate or bivariate data."""
        if x2 is None:
            return self._eval_univariate(x1, weights)
        else:
            return self._eval_bivariate(x1, x2, weights)

class Histogram:
    """Univariate and bivariate histogram estimator."""

    def __init__(self, stat='count', bins='auto', binwidth=None, binrange=None, discrete=False, cumulative=False):
        """Initialize the estimator with its parameters.

        Parameters
        ----------
        stat : str
            Aggregate statistic to compute in each bin.

            - `count`: show the number of observations in each bin
            - `frequency`: show the number of observations divided by the bin width
            - `probability` or `proportion`: normalize such that bar heights sum to 1
            - `percent`: normalize such that bar heights sum to 100
            - `density`: normalize such that the total area of the histogram equals 1

        bins : str, number, vector, or a pair of such values
            Generic bin parameter that can be the name of a reference rule,
            the number of bins, or the breaks of the bins.
            Passed to :func:`numpy.histogram_bin_edges`.
        binwidth : number or pair of numbers
            Width of each bin, overrides ``bins`` but can be used with
            ``binrange``.
        binrange : pair of numbers or a pair of pairs
            Lowest and highest value for bin edges; can be used either
            with ``bins`` or ``binwidth``. Defaults to data extremes.
        discrete : bool or pair of bools
            If True, set ``binwidth`` and ``binrange`` such that bin
            edges cover integer values in the dataset.
        cumulative : bool
            If True, return the cumulative statistic.

        """
        stat_choices = ['count', 'frequency', 'density', 'probability', 'proportion', 'percent']
        _check_argument('stat', stat_choices, stat)
        self.stat = stat
        self.bins = bins
        self.binwidth = binwidth
        self.binrange = binrange
        self.discrete = discrete
        self.cumulative = cumulative
        self.bin_kws = None

    def _define_bin_edges(self, x, weights, bins, binwidth, binrange, discrete):
        """Inner function that takes bin parameters as arguments."""
        pass

    def define_bin_params(self, x1, x2=None, weights=None, cache=True):
        """Given data, return numpy.histogram parameters to define bins."""
        pass

    def _eval_bivariate(self, x1, x2, weights):
        """Inner function for histogram of two variables."""
        pass

    def _eval_univariate(self, x, weights):
        """Inner function for histogram of one variable."""
        pass

    def __call__(self, x1, x2=None, weights=None):
        """Count the occurrences in each bin, maybe normalize."""
        if x2 is None:
            return self._eval_univariate(x1, weights)
        else:
            return self._eval_bivariate(x1, x2, weights)

class ECDF:
    """Univariate empirical cumulative distribution estimator."""

    def __init__(self, stat='proportion', complementary=False):
        """Initialize the class with its parameters

        Parameters
        ----------
        stat : {{"proportion", "percent", "count"}}
            Distribution statistic to compute.
        complementary : bool
            If True, use the complementary CDF (1 - CDF)

        """
        _check_argument('stat', ['count', 'percent', 'proportion'], stat)
        self.stat = stat
        self.complementary = complementary

    def _eval_bivariate(self, x1, x2, weights):
        """Inner function for ECDF of two variables."""
        pass

    def _eval_univariate(self, x, weights):
        """Inner function for ECDF of one variable."""
        pass

    def __call__(self, x1, x2=None, weights=None):
        """Return proportion or count of observations below each sorted datapoint."""
        x1 = np.asarray(x1)
        if weights is None:
            weights = np.ones_like(x1)
        else:
            weights = np.asarray(weights)
        if x2 is None:
            return self._eval_univariate(x1, weights)
        else:
            return self._eval_bivariate(x1, x2, weights)

class EstimateAggregator:

    def __init__(self, estimator, errorbar=None, **boot_kws):
        """
        Data aggregator that produces an estimate and error bar interval.

        Parameters
        ----------
        estimator : callable or string
            Function (or method name) that maps a vector to a scalar.
        errorbar : string, (string, number) tuple, or callable
            Name of errorbar method (either "ci", "pi", "se", or "sd"), or a tuple
            with a method name and a level parameter, or a function that maps from a
            vector to a (min, max) interval, or None to hide errorbar. See the
            :doc:`errorbar tutorial </tutorial/error_bars>` for more information.
        boot_kws
            Additional keywords are passed to bootstrap when error_method is "ci".

        """
        self.estimator = estimator
        method, level = _validate_errorbar_arg(errorbar)
        self.error_method = method
        self.error_level = level
        self.boot_kws = boot_kws

    def __call__(self, data, var):
        """Aggregate over `var` column of `data` with estimate and error interval."""
        vals = data[var]
        if callable(self.estimator):
            estimate = self.estimator(vals)
        else:
            estimate = vals.agg(self.estimator)
        if self.error_method is None:
            err_min = err_max = np.nan
        elif len(data) <= 1:
            err_min = err_max = np.nan
        elif callable(self.error_method):
            err_min, err_max = self.error_method(vals)
        elif self.error_method == 'sd':
            half_interval = vals.std() * self.error_level
            err_min, err_max = (estimate - half_interval, estimate + half_interval)
        elif self.error_method == 'se':
            half_interval = vals.sem() * self.error_level
            err_min, err_max = (estimate - half_interval, estimate + half_interval)
        elif self.error_method == 'pi':
            err_min, err_max = _percentile_interval(vals, self.error_level)
        elif self.error_method == 'ci':
            units = data.get('units', None)
            boots = bootstrap(vals, units=units, func=self.estimator, **self.boot_kws)
            err_min, err_max = _percentile_interval(boots, self.error_level)
        return pd.Series({var: estimate, f'{var}min': err_min, f'{var}max': err_max})

class WeightedAggregator:

    def __init__(self, estimator, errorbar=None, **boot_kws):
        """
        Data aggregator that produces a weighted estimate and error bar interval.

        Parameters
        ----------
        estimator : string
            Function (or method name) that maps a vector to a scalar. Currently
            supports only "mean".
        errorbar : string or (string, number) tuple
            Name of errorbar method or a tuple with a method name and a level parameter.
            Currently the only supported method is "ci".
        boot_kws
            Additional keywords are passed to bootstrap when error_method is "ci".

        """
        if estimator != 'mean':
            raise ValueError(f"Weighted estimator must be 'mean', not {estimator!r}.")
        self.estimator = estimator
        method, level = _validate_errorbar_arg(errorbar)
        if method is not None and method != 'ci':
            raise ValueError(f"Error bar method must be 'ci', not {method!r}.")
        self.error_method = method
        self.error_level = level
        self.boot_kws = boot_kws

    def __call__(self, data, var):
        """Aggregate over `var` column of `data` with estimate and error interval."""
        vals = data[var]
        weights = data['weight']
        estimate = np.average(vals, weights=weights)
        if self.error_method == 'ci' and len(data) > 1:

            def error_func(x, w):
                return np.average(x, weights=w)
            boots = bootstrap(vals, weights, func=error_func, **self.boot_kws)
            err_min, err_max = _percentile_interval(boots, self.error_level)
        else:
            err_min = err_max = np.nan
        return pd.Series({var: estimate, f'{var}min': err_min, f'{var}max': err_max})

class LetterValues:

    def __init__(self, k_depth, outlier_prop, trust_alpha):
        """
        Compute percentiles of a distribution using various tail stopping rules.

        Parameters
        ----------
        k_depth: "tukey", "proportion", "trustworthy", or "full"
            Stopping rule for choosing tail percentiled to show:

            - tukey: Show a similar number of outliers as in a conventional boxplot.
            - proportion: Show approximately `outlier_prop` outliers.
            - trust_alpha: Use `trust_alpha` level for most extreme tail percentile.

        outlier_prop: float
            Parameter for `k_depth="proportion"` setting the expected outlier rate.
        trust_alpha: float
            Parameter for `k_depth="trustworthy"` setting the confidence threshold.

        Notes
        -----
        Based on the proposal in this paper:
        https://vita.had.co.nz/papers/letter-value-plot.pdf

        """
        k_options = ['tukey', 'proportion', 'trustworthy', 'full']
        if isinstance(k_depth, str):
            _check_argument('k_depth', k_options, k_depth)
        elif not isinstance(k_depth, int):
            err = f'The `k_depth` parameter must be either an integer or string (one of {k_options}), not {k_depth!r}.'
            raise TypeError(err)
        self.k_depth = k_depth
        self.outlier_prop = outlier_prop
        self.trust_alpha = trust_alpha

    def __call__(self, x):
        """Evaluate the letter values."""
        k = self._compute_k(len(x))
        exp = (np.arange(k + 1, 1, -1), np.arange(2, k + 2))
        levels = k + 1 - np.concatenate([exp[0], exp[1][1:]])
        percentiles = 100 * np.concatenate([0.5 ** exp[0], 1 - 0.5 ** exp[1]])
        if self.k_depth == 'full':
            percentiles[0] = 0
            percentiles[-1] = 100
        values = np.percentile(x, percentiles)
        fliers = np.asarray(x[(x < values.min()) | (x > values.max())])
        median = np.percentile(x, 50)
        return {'k': k, 'levels': levels, 'percs': percentiles, 'values': values, 'fliers': fliers, 'median': median}

def _percentile_interval(data, width):
    """Return a percentile interval from data of a given width."""
    pass

def _validate_errorbar_arg(arg):
    """Check type and value of errorbar argument and assign default level."""
    pass