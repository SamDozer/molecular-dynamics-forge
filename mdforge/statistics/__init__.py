"""Statistics: descriptive stats, time-series helpers, correlation, bootstrap CIs."""

from mdforge.statistics.descriptive import describe, summary_frame, bootstrap_ci  # noqa: F401
from mdforge.statistics.timeseries import (  # noqa: F401
    moving_average, rolling_std, running_mean, block_average, block_average_sem,
    plateau_detection,
)
from mdforge.statistics.correlation import correlation_matrices  # noqa: F401
