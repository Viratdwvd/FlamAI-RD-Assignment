import numpy as np

from src.model import generate_curve
from src.objective import mean_squared_error, residual_vector


def test_residual_vector_is_zero_for_true_parameters():
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

    result = residual_vector(
        x=x,
        y=y,
        theta=theta,
        m=m,
        x_offset=x_offset,
    )

    np.testing.assert_allclose(result, 0.0, atol=1e-10)


def test_mse_is_zero_for_true_parameters():
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

    error = mean_squared_error(
        x=x,
        y=y,
        theta=theta,
        m=m,
        x_offset=x_offset,
    )

    assert error < 1e-20


def test_wrong_parameters_have_nonzero_error():
    t = np.linspace(-5, 5, 100)

    x, y = generate_curve(
        t=t,
        theta=0.4,
        m=0.01,
        x_offset=55.0,
    )

    error = mean_squared_error(
        x=x,
        y=y,
        theta=0.8,
        m=0.02,
        x_offset=60.0,
    )

    assert error > 1e-6