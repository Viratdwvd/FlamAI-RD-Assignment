import numpy as np

from src.model import generate_curve


def test_generate_curve_shape():
    t = np.linspace(-5, 5, 100)

    x, y = generate_curve(
        t=t,
        theta=0.5,
        m=0.01,
        x_offset=55.0,
    )

    assert x.shape == t.shape
    assert y.shape == t.shape


def test_generate_curve_is_finite():
    t = np.linspace(-5, 5, 100)

    x, y = generate_curve(
        t=t,
        theta=0.5,
        m=0.01,
        x_offset=55.0,
    )

    assert np.isfinite(x).all()
    assert np.isfinite(y).all()