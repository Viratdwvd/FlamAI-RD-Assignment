import numpy as np


Y_OFFSET = 42.0
OSCILLATION_FREQUENCY = 0.3


def generate_curve(
    t: np.ndarray,
    theta: float,
    m: float,
    x_offset: float,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate x and y coordinates from the FlamAI parametric model.

    Parameters
    ----------
    t:
        Parameter values.
    theta:
        Rotation angle in radians.
    m:
        Exponential growth/decay parameter.
    x_offset:
        Horizontal translation.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Generated x and y coordinates.
    """
    oscillation = np.exp(m * np.abs(t)) * np.sin(
        OSCILLATION_FREQUENCY * t
    )

    x = (
        t * np.cos(theta)
        - oscillation * np.sin(theta)
        + x_offset
    )

    y = (
        Y_OFFSET
        + t * np.sin(theta)
        + oscillation * np.cos(theta)
    )

    return x, y