import numpy as np
from scipy.optimize import least_squares

from src.data_loader import load_data
from src.inverse import residuals


THETA_BOUNDS = (0.0, np.deg2rad(50.0))
M_BOUNDS = (-0.05, 0.05)
X_BOUNDS = (0.0, 100.0)


def fit_parameters(path: str) -> dict[str, float]:
    """Estimate theta, M and X from the observed XY data."""

    df = load_data(path)

    x = df["x"].to_numpy(dtype=float)
    y = df["y"].to_numpy(dtype=float)

    def objective(params: np.ndarray) -> np.ndarray:
        theta, m, x_offset = params

        return residuals(
            x=x,
            y=y,
            theta=theta,
            m=m,
            x_offset=x_offset,
        )

    initial_guess = np.array([
        np.deg2rad(25.0),
        0.0,
        50.0,
    ])

    lower_bounds = np.array([
        THETA_BOUNDS[0],
        M_BOUNDS[0],
        X_BOUNDS[0],
    ])

    upper_bounds = np.array([
        THETA_BOUNDS[1],
        M_BOUNDS[1],
        X_BOUNDS[1],
    ])

    result = least_squares(
        objective,
        x0=initial_guess,
        bounds=(lower_bounds, upper_bounds),
    )

    theta, m, x_offset = result.x

    return {
        "theta_radians": float(theta),
        "theta_degrees": float(np.rad2deg(theta)),
        "M": float(m),
        "X": float(x_offset),
        "cost": float(result.cost),
    }


if __name__ == "__main__":
    parameters = fit_parameters("data/xy_data.csv")

    print("Estimated parameters:")
    print(f"theta = {parameters['theta_radians']:.10f} rad")
    print(f"theta = {parameters['theta_degrees']:.10f} degrees")
    print(f"M     = {parameters['M']:.10f}")
    print(f"X     = {parameters['X']:.10f}")
    print(f"cost  = {parameters['cost']:.10e}")