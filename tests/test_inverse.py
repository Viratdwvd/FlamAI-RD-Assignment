import numpy as np

from src.inverse import inverse_transform, residuals
from src.model import generate_curve


def test_inverse_transform_recovers_original_components():
    t = np.linspace(-5, 5, 100)

    theta = 0.4
    m = 0.01
    x_offset = 55.0

    x, y = generate_curve(
        t=t,
        theta=theta,
        m=m,
        x_offset=x_offset,
    )

    recovered_t, recovered_oscillation = inverse_transform(
        x=x,
        y=y,
        theta=theta,
        x_offset=x_offset,
    )

    expected_oscillation = (
        np.exp(m * np.abs(t))
        * np.sin(0.3 * t)
    )

    np.testing.assert_allclose(recovered_t, t)
    np.testing.assert_allclose(
        recovered_oscillation,
        expected_oscillation,
    )


def test_residuals_are_zero_for_matching_parameters():
    t = np.linspace(-5, 5, 100)

    theta = 0.4
    m = 0.01
    x_offset = 55.0

    x, y = generate_curve(
        t=t,
        theta=theta,
        m=m,
        x_offset=x_offset,
    )

    result = residuals(
        x=x,
        y=y,
        theta=theta,
        m=m,
        x_offset=x_offset,
    )

    np.testing.assert_allclose(result, 0.0, atol=1e-10)