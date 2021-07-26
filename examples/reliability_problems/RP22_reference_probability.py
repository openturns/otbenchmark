#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author : Régis Lebrun, Feb 2021.

The reference value 0.00416 is wrong and should be
replaced by 0.004207305511299617942000431.
The following script presents two methods to compute it using OT.

The output is:

(Maple)               P= 0.004207305511299618
(Iterated quadrature) P= 0.004207306989391163
(Gauss Kronrod)       P= 0.004207305511305987
"""


import openturns as ot
from math import sqrt, exp

# P = P(2.5 - 1 / sqrt(2) * (x1 + x2) + 0.1 * (x1 - x2) ^2<0)
# It can be rewritten as:
# P = \int_{x1_0}^{\infty}\int_{5\sqrt{2}/2+x1
#    -\sqrt{-50+40\sqrt{2}x1}/2}^{5\sqrt{2}/2+x1
#    +\sqrt{-50+40\sqrt{2}x1}/2}\phi(x1)\phi(x2)dx2dx1
# where x1_0=5\sqrt{2}/8~0.883883476483184405501055452631
# Maple gives P=0.420730551129961794200043418946e-2
print("(Maple)               P=", 0.420730551129961794200043418946e-2)
lower = ot.SymbolicFunction("x1", "5*sqrt(2)/2+x1-sqrt(-50+40*sqrt(2)*x1)/2")
upper = ot.SymbolicFunction("x1", "5*sqrt(2)/2+x1+sqrt(-50+40*sqrt(2)*x1)/2")
x1_0 = 5 * sqrt(2) / 8


def kernel(X):
    return [ot.Normal(2).computePDF(X)]


P = ot.IteratedQuadrature().integrate(
    ot.PythonFunction(2, 1, kernel), x1_0, 10.0, [lower], [upper]
)[0]
print("(Iterated quadrature) P=", P)
# The innermost integral has a closed-form:
# P = \int_{x1_0}^{\infty}Phi(5\sqrt{2}/2+x1+\sqrt{-50+40\sqrt{2}x1}/2)
#     -Phi(5\sqrt{2}/2+x1-\sqrt{-50+40\sqrt{2}x1}/2)\phi(x1)dx1


def f(x):
    x1 = x[0]
    pnormal1 = ot.DistFunc.pNormal(
        5 * sqrt(2) / 2 + x1 + sqrt(-50 + 40 * sqrt(2) * x1) / 2
    )
    pnormal2 = ot.DistFunc.pNormal(
        5 * sqrt(2) / 2 + x1 - sqrt(-50 + 40 * sqrt(2) * x1) / 2
    )
    return [(pnormal1 - pnormal2) * exp(-(x1 ** 2) / 2) * ot.SpecFunc.ISQRT2PI]


P = ot.GaussKronrod().integrate(ot.PythonFunction(1, 1, f), ot.Interval(x1_0, 10.0))[0]
print("(Gauss Kronrod)       P=", P)
