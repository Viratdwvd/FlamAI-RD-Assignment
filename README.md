
with domain `6 ≤ t ≤ 60`. Pasting this into Desmos parametric graphing
reproduces the observed curve exactly (see Desmos link above).

### Validation Results

Running `src/validate.py` against the 1500 observed points gives:

| Metric | Value |
|---|---:|
| Observed points | 1500 |
| Uniformly sampled comparison points | 1497 |
| **L1 distance** | **1.469 × 10⁻⁴** |
| RMSE | 3.96 × 10⁻⁴ |

Both figures are effectively zero relative to the data's scale (x, y ~ 46–110),
confirming the recovered parameters reproduce the ground-truth curve almost exactly.

**Raw observed data:**

![Observed XY data](results/raw_data.png)

**Recovered curve overlaid on observed data:**

![Fitted curve vs observed data](results/fitted_curve.png)

### How to Reproduce

```bash
pip install -r requirements.txt

# Recover theta, M, X from data/xy_data.csv
python -m src.fit

# Validate the fit (L1/RMSE + generates results/fitted_curve.png)
python -m src.validate

# Run the test suite
pytest tests/
```

---

## 3. Mathematical Reformulation

Define the translated coordinates:

\[
u=x-X
\]

\[
v=y-42
\]

The original equations become:

\[
u=t\cos(\theta)
-e^{M|t|}\sin(0.3t)\sin(\theta)
\]

\[
v=t\sin(\theta)
+e^{M|t|}\sin(0.3t)\cos(\theta)
\]

Applying the inverse rotation gives:

\[
t=u\cos(\theta)+v\sin(\theta)
\]

and

\[
r=-u\sin(\theta)+v\cos(\theta)
\]

Therefore:

\[
r=e^{M|t|}\sin(0.3t)
\]

This transformation separates the approximately linear coordinate `t`
from the oscillatory component `r`.

---

## 4. Residual Formulation

For a candidate parameter vector

\[
p=(\theta,M,X)
\]

the transformed observations are:

\[
t_i=(x_i-X)\cos(\theta)+(y_i-42)\sin(\theta)
\]

\[
r_i=-(x_i-X)\sin(\theta)+(y_i-42)\cos(\theta)
\]

The model predicts:

\[
\hat r_i=e^{M|t_i|}\sin(0.3t_i)
\]

The residual for each observation is:

\[
\epsilon_i=r_i-\hat r_i
\]

The parameters are estimated by minimizing these residuals subject to
the specified parameter bounds.

---

## 5. Parameter Estimation

The parameter recovery problem is solved as a bounded nonlinear least-squares
optimization using `scipy.optimize.least_squares`.

The optimizer estimates:

- \(\theta\): rotation angle
- \(M\): exponential growth/decay parameter
- \(X\): horizontal translation

The optimization respects the parameter bounds specified in the assignment:

\[
0^\circ < \theta < 50^\circ
\]

\[
-0.05 < M < 0.05
\]

\[
0 < X < 100
\]

The implementation is contained in:

```text
src/fit.py
src/objective.py
src/model.py
src/inverse.py
```