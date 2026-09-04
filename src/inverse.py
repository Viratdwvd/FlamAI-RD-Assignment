import numpy as np


Y_OFFSET = 42.0
OSCILLATION_FREQUENCY = 0.3


def inverse_transform(
    x: np.ndarray,
    y: np.ndarray,
    theta: float,
    x_offset: float,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Reverse the rotation and translation applied by the parametric model.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Recovered t and oscillatory component A(t).
    """
    u = x - x_offset
    v = y - Y_OFFSET

    t = u * np.cos(theta) + v * np.sin(theta)
    oscillation = -u * np.sin(theta) + v * np.cos(theta)

    return t, oscillation


def residuals(
    x: np.ndarray,
    y: np.ndarray,
    theta: float,
    m: float,
    x_offset: float,
) -> np.ndarray:
    """
    Compute model residuals for a candidate parameter set.
    """
    t, observed_oscillation = inverse_transform(
        x=x,
        y=y,
        theta=theta,
        x_offset=x_offset,
    )

    predicted_oscillation = (
        np.exp(m * np.abs(t))
        * np.sin(OSCILLATION_FREQUENCY * t)
    )

    return observed_oscillation - predicted_oscillation