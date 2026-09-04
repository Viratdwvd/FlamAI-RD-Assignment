# FlamAI R&D Assignment — Parametric Curve Parameter Recovery
- **Desmos link:** https://www.desmos.com/calculator/mxidc3gcwo
## 1. Objective

The objective of this assignment is to recover the three unknown parameters
`θ`, `M`, and `X` from the provided `xy_data.csv` dataset.

The given parametric curve is:

\[
x(t)=t\cos(\theta)
-e^{M|t|}\sin(0.3t)\sin(\theta)+X
\]

\[
y(t)=42+t\sin(\theta)
+e^{M|t|}\sin(0.3t)\cos(\theta)
\]

with the constraints:

\[
0^\circ < \theta < 50^\circ
\]

\[
-0.05 < M < 0.05
\]

\[
0 < X < 100
\]

and

\[
6 < t < 60
\]

The dataset contains 1500 observed `(x,y)` points.

---

## 2. Solution

The recovered parameters are:

| Parameter | Recovered value |
|---|---:|
| θ | **30.0000000000°** |
| θ | **0.5235987756 rad** |
| M | **0.0300000000** |
| X | **55.0000000000** |

Therefore, the final parameter values are:

\[
\boxed{\theta=30^\circ}
\]

\[
\boxed{M=0.03}
\]

\[
\boxed{X=55}
\]

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