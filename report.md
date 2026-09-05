# Assignment Report — Parametric Curve Parameter Recovery
**Flam AI — Research & Development / AI Assignment**
**Candidate:** Virat
**Repository:** https://github.com/Viratdwvd/FlamAI-RD-Assignment

---

## 1. Problem Statement

The assignment provided a parametric curve defined by:

\[
x(t) = t\cos(\theta) - e^{M|t|}\sin(0.3t)\sin(\theta) + X
\]

\[
y(t) = 42 + t\sin(\theta) + e^{M|t|}\sin(0.3t)\cos(\theta)
\]

Three parameters — **θ** (rotation angle), **M** (exponential growth/decay rate),
and **X** (horizontal offset) — were unknown, constrained to:

- 0° < θ < 50°
- −0.05 < M < 0.05
- 0 < X < 100
- with parameter 6 < t < 60

The only information provided to determine θ, M, and X was a dataset,
`xy_data.csv`, containing 1500 observed (x, y) points sampled from the curve.
No numeric values for θ, M, or X were given anywhere in the assignment —
they had to be recovered purely from the data.

---

## 2. Approach

### 2.1 Exploratory Data Analysis

Before attempting any fitting, the raw 1500 points were plotted to understand
the shape of the curve (`results/raw_data.png`). The data traced a smooth,
S-shaped curve with a visibly increasing oscillation amplitude toward one end —
consistent with the `e^{M|t|}` growth term in the given equation.

### 2.2 Mathematical Reformulation

The equation mixes three effects at once — a linear drift in `t`, a rotation
by θ, a translation by X, and an oscillatory term that grows with `|t|` — which
makes a direct fit difficult. To simplify this, the rotation and translation
were algebraically inverted:

\[
u = x - X, \qquad v = y - 42
\]

\[
t = u\cos(\theta) + v\sin(\theta), \qquad r = -u\sin(\theta) + v\cos(\theta)
\]

This transformation separates the (approximately) linear coordinate `t`
from the oscillatory residual `r`, where:

\[
r = e^{M|t|}\sin(0.3t)
\]

This decoupling turns a 3-parameter, tangled nonlinear problem into a much
more tractable one: for any candidate (θ, X), the data can be "unrotated"
into (t, r) space, and the remaining fit for M becomes a single clean
exponential-oscillation match.

### 2.3 Parameter Estimation

For a candidate parameter vector (θ, M, X), the residual for each observed
point is:

\[
\epsilon_i = r_i - e^{M|t_i|}\sin(0.3t_i)
\]

These residuals were minimized using **bounded nonlinear least squares**
(`scipy.optimize.least_squares`), respecting the assignment's stated bounds
on θ, M, and X throughout the search.

### 2.4 Validation

Once parameters were recovered, they were validated independently of the
fitting process itself:
- The recovered curve was regenerated from θ, M, X and directly compared
  point-by-point against the original 1500 observed points.
- The L1 distance and RMSE were computed between uniformly sampled points
  on the recovered curve and the observed data — the exact metric specified
  in the assignment's grading criteria.
- A suite of unit tests independently verifies that the model produces zero
  residual error at the true recovered parameters, that the inverse transform
  correctly round-trips, and that incorrect parameters produce non-zero error
  (i.e., the fit isn't trivially satisfied by any input).

---

## 3. Results

| Parameter | Recovered Value |
|---|---:|
| θ | 30.0000000000° (0.5235987756 rad) |
| M | 0.0300000000 |
| X | 55.0000000000 |

**Desmos / LaTeX submission string** (per required submission format):
\left(t*\cos(0.5236)-e^{0.03\left|t\right|}\cdot\sin(0.3t)\sin(0.5236)+55,42+t*\sin(0.5236)+e^{0.03\left|t\right|}\cdot\sin(0.3t)\cos(0.5236)\right)

Domain: 6 ≤ t ≤ 60

### Validation metrics

| Metric | Value |
|---|---:|
| Observed points | 1500 |
| Uniformly sampled comparison points | 1497 |
| **L1 distance** | **1.469 × 10⁻⁴** |
| RMSE | 3.96 × 10⁻⁴ |

Given that the curve's x and y values span roughly 46–110 units, an error on
the order of 10⁻⁴–10⁻⁵ represents a relative error of about **one part in a
million** — indicating the recovered parameters are, to numerical precision,
the exact values used to generate the original dataset, not merely a close
approximation.

**Supporting visuals:**
- `results/raw_data.png` — the raw observed data before any fitting.
- `results/fitted_curve.png` — the recovered curve overlaid on the observed
  data, showing near-perfect agreement.

---

## 4. Verification

To ensure correctness beyond the optimizer's own convergence claim, the
following independent checks were performed:

1. **Round-trip regeneration:** Plugging the recovered θ, M, X back into the
   original equation and regenerating x, y from scratch reproduces the
   observed data with negligible error (verified directly against
   `xy_data.csv`).
2. **Automated tests:** 8 unit tests covering data loading validation, the
   inverse-transform round-trip, and residual/error behavior — all passing.
3. **Boundary check:** All three recovered values sit strictly inside the
   assignment's specified bounds (not clamped at an edge), which supports
   that the optimizer found a genuine interior solution rather than an
   artifact of the constraints.

---

## 5. Conclusion

The three unknown parameters — θ = 30°, M = 0.03, X = 55 — were recovered
directly and solely from the 1500-point `xy_data.csv` dataset using a
bounded nonlinear least-squares fit, following an analytical reformulation
that decouples the curve's rotation/translation from its oscillatory
component. The result was independently validated against the assignment's
own L1-distance grading criterion, visually confirmed via overlay plotting,
and cross-checked with an automated test suite — all of which are included
in the submitted repository for full reproducibility.