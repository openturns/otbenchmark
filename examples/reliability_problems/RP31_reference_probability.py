#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author : Régis Lebrun, Feb 2021.
The reference value P=0.00018 should be replaced
by 0.003226681209587691 as shown here.

The output is:

(distribution arithmetic) P= 0.0031946106908761515
(Maple)                   P= 0.003226681209587691
(Iterated quadrature)     P= 0.0032266812122437333
(Gauss Kronrod)           P= 0.0032266812095876935
(Hermite quadrature)      P= 0.0032260402746775926
"""

import openturns as ot
from math import exp

# A first try is to use distribution arithmetic, which gives poor
# results as the characteristic function of x1^4 is not known exactly
# and its PDF is infinite at 0
# Here are the ResourceMap keys to play with...
# ot.ResourceMap.SetAsUnsignedInteger(
#    "Distribution-CharacteristicFunctionNMax", 10000000)
# ot.ResourceMap.SetAsUnsignedInteger(
#    "Distribution-DefaultIntegrationNodesNumber", 128)
# ot.ResourceMap.SetAsScalar(
#    "GaussKronrod-MaximumError",  1.0e-10)
# ot.ResourceMap.SetAsUnsignedInteger(
#    "GaussKronrod-MaximumSubIntervals", 100000)
x1 = ot.Normal()
x2 = ot.Normal()
y = 2 - x2 + 256 * x1.sqr().sqr()  # x1**4 has a bug...
print("(distribution arithmetic) P=", y.computeCDF(0.0))
# The probability is equal to
# P=\int_{-\infty}^\infty \int_{2+256*x1^4}^\infty \phi(xi)\phi(x2)dx2dx1
# Maple gives P=0.322668120958769103770120768386e-2
print("(Maple)                   P=", 0.322668120958769103770120768386e-2)
lower = ot.SymbolicFunction("x1", "2+256*x1^4")
upper = ot.SymbolicFunction("x1", "8.5")


def kernel(X):
    return [ot.Normal(2).computePDF(X)]


P = ot.IteratedQuadrature().integrate(
    ot.PythonFunction(2, 1, kernel), -8.5, 8.5, [lower], [upper]
)[0]
print("(Iterated quadrature)     P=", P)
# It can be rewritten as:
# P=\int_{-\infty}^\infty \phi(x1)(1-Phi(2+256*x1^4))dx1
# This way it can be computed using either Gauss-Kronrod
# on \phi(x1)(1-Phi(2+256*x1^4)) over e.g. [-8.5,8.5]


def f1(x1):
    x = x1[0]
    pnormal = ot.DistFunc.pNormal(2 + 256 * x ** 4, True)
    return [exp(-(x ** 2) / 2) * ot.SpecFunc.ISQRT2PI * pnormal]


P = ot.GaussKronrod().integrate(ot.PythonFunction(1, 1, f1), ot.Interval(-8.5, 8.5))[0]
print("(Gauss Kronrod)           P=", P)
# or an Hermite quadrature on (1-Phi(2+256*x1^4))
# This method is VERY inefficient as the function we integrate is badly
# approximated by polynomials (it has finite limits at x=+/-inf
# so we have to use an indecent number of quadrature points to get 4 correct
# digits


def f2(x):
    return [ot.DistFunc.pNormal(2 + 256 * x[0] ** 4, True)]


xi, w = ot.GaussProductExperiment(ot.Normal(), [2000]).generateWithWeights()
P = sum([y_i[0] * w_i for (y_i, w_i) in zip(ot.PythonFunction(1, 1, f2)(xi), w)])
print("(Hermite quadrature)      P=", P)
