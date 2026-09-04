\# FlamAI R\&D Assignment



Parameter estimation and parametric curve reconstruction for the FlamAI Research \& Development assignment.



\## Objective



Recover the unknown parameters `θ`, `M`, and `X` from the provided XY dataset using the parametric curve specified in the assignment.



\## Project Status



\- \[x] Project setup

\- \[ ] Dataset analysis

\- \[ ] Mathematical formulation

\- \[ ] Parameter estimation

\- \[ ] Curve validation

\- \[ ] Visualization

\- \[ ] Testing

\- \[ ] Final documentation

# FlamAI R&D Assignment — Parametric Curve Parameter Recovery

## 1. Problem Statement

The objective of this assignment is to recover the three unknown parameters
\(\theta\), \(M\), and \(X\) from a set of observed \((x,y)\) points generated
by the following parametric curve:

\[
x(t)=t\cos(\theta)
-e^{M|t|}\sin(0.3t)\sin(\theta)+X
\]

\[
y(t)=42+t\sin(\theta)
+e^{M|t|}\sin(0.3t)\cos(\theta)
\]

with:

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

The supplied `xy_data.csv` contains 1500 points lying on the curve.

---

## 2. Approach

The parameter recovery was treated as a bounded nonlinear least-squares
optimization problem.

### Step 1 — Data Loading and Validation

The dataset is loaded using `src/data_loader.py`.

The loader verifies:

- Required columns are exactly `x` and `y`
- Dataset is non-empty
- Both columns are numeric
- No missing values are present
- No duplicate rows are present

---

## 3. Geometric Reformulation

The parametric equations can be written as a rotated coordinate system.

Define:

\[
u = x-X
\]

\[
v = y-42
\]

The equations become:

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

This inverse transformation is useful because it separates the approximately
linear coordinate \(t\) from the oscillatory/exponential component.

---

## 4. Residual Formulation

For a candidate parameter vector

\[
p=(\theta,M,X)
\]

the transformed observations produce:

\[
t_i=(x_i-X)\cos(\theta)+(y_i-42)\sin(\theta)
\]

and

\[
r_i=-(x_i-X)\sin(\theta)+(y_i-42)\cos(\theta)
\]

The model predicts:

\[
\hat r_i=e^{M|t_i|}\sin(0.3t_i)
\]

The residual used for optimization is:

\[
\epsilon_i=r_i-\hat r_i
\]

The objective is therefore to minimize the residual error while respecting the
given parameter bounds.

---

## 5. Parameter Estimation

The implementation uses bounded nonlinear least squares with
`scipy.optimize.least_squares`.

A geometric initialization is used to provide a good starting point for the
optimizer:

- \(\theta\) is estimated from the dominant orientation of the curve.
- \(M\) is initialized using the exponential envelope after transforming the
  observations.
- \(X\) is initialized from the horizontal translation.

The optimizer then refines all three parameters jointly.

Implementation:

```text
src/model.py
src/inverse.py
src/objective.py
src/fit.py