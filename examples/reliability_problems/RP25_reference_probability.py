#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author : Régis Lebrun, Feb 2021.

The reference value P=0.00000614 should be replaced by
0.0023886702326968586 as shown here.

The output is:

(Maple)               P= 4.148566293759747e-05
(Iterated quadrature) P= 4.1485683826245365e-05
(Gauss Kronrod)       P= 4.148566293759749e-05
"""

import openturns as ot
from math import sqrt, exp

# P = P(max(x1^2-8x2+16,-16x1+x2+32)<0)
# It can be rewritten as:
# P = \int_{x1_0}^\{x1_1}\int_{2+x1^2/8}^{16x1-32}\phi(x1)\phi(x2)dx2dx1
# where x1_0 and x1_1 solve 16*x1_0-32=2+x1^2/8 i.e.
# x1_0=64-4sqrt(239)~2.1615006650387739213966284668
# x1_1=64-4sqrt(239)~125.838499334961226078603371533
# Maple gives P=0.41485662937597470791345e-4
print("(Maple)               P=", 0.41485662937597470791345e-4)
lower = ot.SymbolicFunction("x1", "2+x1^2/8")
upper = ot.SymbolicFunction("x1", "16*x1-32")
x1_0 = 64 - 4 * sqrt(239)
x1_1 = 64 + 4 * sqrt(239)


def kernel(X):
    return [ot.Normal(2).computePDF(X)]


P = ot.IteratedQuadrature().integrate(
    ot.PythonFunction(2, 1, kernel), x1_0, x1_1, [lower], [upper]
)[0]
print("(Iterated quadrature) P=", P)
# We can also rewrite the 2D integrals into a 1D integrale
# P = \int_{x1_0}^{X1_1}(Phi(16*x1-32)-Phi(2+x1^2/8))\phi(x1)dx1


def f(x):
    pnormal1 = ot.DistFunc.pNormal(16 * x[0] - 32)
    pnormal2 = ot.DistFunc.pNormal(2 + x[0] ** 2 / 8)
    return [(pnormal1 - pnormal2) * exp(-x[0] ** 2 / 2) * ot.SpecFunc.ISQRT2PI]


P = ot.GaussKronrod().integrate(ot.PythonFunction(1, 1, f), ot.Interval(x1_0, x1_1))[0]
print("(Gauss Kronrod)       P=", P)
