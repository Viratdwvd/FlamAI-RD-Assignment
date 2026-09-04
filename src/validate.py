import numpy as np
import matplotlib.pyplot as plt

from src.data_loader import load_data
from src.model import generate_curve


T_MIN = 6.0
T_MAX = 60.0

THETA = np.deg2rad(30.0)
M = 0.03
X_OFFSET = 55.0


def generate_uniform_curve(
    theta: float,
    m: float,
    x_offset: float,
    n_points: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate uniformly sampled points on the parametric curve."""

    t = np.linspace(T_MIN, T_MAX, n_points)

    return generate_curve(
        t=t,
        theta=theta,
        m=m,
        x_offset=x_offset,
    )


def l1_distance(
    observed_y: np.ndarray,
    predicted_y: np.ndarray,
) -> float:
    """Calculate mean L1 distance between corresponding curve values."""

    return float(np.mean(np.abs(observed_y - predicted_y)))


def plot_comparison(
    observed_x: np.ndarray,
    observed_y: np.ndarray,
    predicted_x: np.ndarray,
    predicted_y: np.ndarray,
) -> None:
    """Plot observed data against the recovered curve."""

    plt.figure(figsize=(10, 6))

    plt.scatter(
        observed_x,
        observed_y,
        s=8,
        label="Observed data",
    )

    plt.plot(
        predicted_x,
        predicted_y,
        linewidth=2,
        label="Recovered curve",
    )

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Observed Data vs Recovered Parametric Curve")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        "results/fitted_curve.png",
        dpi=150,
    )

    plt.show()


if __name__ == "__main__":
    df = load_data("data/xy_data.csv")

    observed_x = df["x"].to_numpy(dtype=float)
    observed_y = df["y"].to_numpy(dtype=float)

    # The CSV points are unordered.
    # Sort them by x to reconstruct the observed geometric curve.
    sort_idx = np.argsort(observed_x)

    observed_x = observed_x[sort_idx]
    observed_y = observed_y[sort_idx]

    # Generate a dense representation of the recovered parametric curve.
    predicted_x, predicted_y = generate_uniform_curve(
        theta=THETA,
        m=M,
        x_offset=X_OFFSET,
        n_points=5000,
    )

    # Determine the common x-domain.
    x_min = max(observed_x.min(), predicted_x.min())
    x_max = min(observed_x.max(), predicted_x.max())

    # Uniformly sample the recovered curve in parameter t.
    t_uniform = np.linspace(
        T_MIN,
        T_MAX,
        1500,
    )

    uniform_x, uniform_y = generate_curve(
        t=t_uniform,
        theta=THETA,
        m=M,
        x_offset=X_OFFSET,
    )

    # Keep only points inside the common observed x-domain.
    mask = (
        (uniform_x >= x_min)
        & (uniform_x <= x_max)
    )

    uniform_x = uniform_x[mask]
    uniform_y = uniform_y[mask]

    # Interpolate the observed curve at the same x locations.
    observed_y_interp = np.interp(
        uniform_x,
        observed_x,
        observed_y,
    )

    predicted_y_interp = uniform_y

    # Calculate L1 distance.
    l1 = l1_distance(
        observed_y_interp,
        predicted_y_interp,
    )

    # Calculate RMSE as an additional diagnostic.
    rmse = float(
        np.sqrt(
            np.mean(
                (observed_y_interp - predicted_y_interp) ** 2
            )
        )
    )

    print("Recovered parameters:")
    print(f"theta = {THETA:.10f} rad")
    print(f"theta = {np.rad2deg(THETA):.10f} degrees")
    print(f"M     = {M:.10f}")
    print(f"X     = {X_OFFSET:.10f}")

    print("\nValidation:")
    print(f"Observed points  : {len(df)}")
    print(f"Comparison points: {len(uniform_x)}")
    print(f"L1 distance      : {l1:.10e}")
    print(f"RMSE             : {rmse:.10e}")

    print("\nObserved ranges:")
    print(f"x: {observed_x.min():.4f} -> {observed_x.max():.4f}")
    print(f"y: {observed_y.min():.4f} -> {observed_y.max():.4f}")

    print("\nPredicted ranges:")
    print(f"x: {predicted_x.min():.4f} -> {predicted_x.max():.4f}")
    print(f"y: {predicted_y.min():.4f} -> {predicted_y.max():.4f}")

    plot_comparison(
        observed_x,
        observed_y,
        predicted_x,
        predicted_y,
    )