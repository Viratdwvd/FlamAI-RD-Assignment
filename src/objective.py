import numpy as np

from src.inverse import residuals


def residual_vector(
    x: np.ndarray,
    y: np.ndarray,
    theta: float,
    m: float,
    x_offset: float,
) -> np.ndarray:
    """Return residuals for a candidate parameter set."""
    return residuals(
        x=x,
        y=y,
        theta=theta,
        m=m,
        x_offset=x_offset,
    )


def mean_squared_error(
    x: np.ndarray,
    y: np.ndarray,
    theta: float,
    m: float,
    x_offset: float,
) -> float:
    """Return the mean squared residual error."""
    r = residual_vector(
        x=x,
        y=y,
        theta=theta,
        m=m,
        x_offset=x_offset,
    )

    return float(np.mean(r ** 2))