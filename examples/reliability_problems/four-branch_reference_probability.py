#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author : Régis Lebrun, Feb 2021.

The reference value beta=2.85 (P=0.002185961454913241)
should be replaced by beta=2.8446811356669155 (P=0.0022227950661944398)
as shown by the script.

The output is:

(Maple)                   P= 0.0022227950661944398
beta= 2.8446811356669155
(Iterated quadrature)     P= 0.002222795065165206
(Gauss Kronrod)           P= 0.0022227950661932727
"""


import openturns as ot
from math import exp

# P = P(min(3 + 0.1 * (x0 - x1)^2 - (x0 + x1) / sqrt(2),
#           3 + 0.1 * (x0 - x1)^2 + (x0 + x1) / sqrt(2),
#           x0 - x1 + 7 / sqrt(2), x1 - x0 + 7 / sqrt(2))<0)
# Using u=(x0-x1)/sqrt(2) and v=(x0+x1)/sqrt(2) and the fact that
# if x1,x2~N(0,1) and are independent, u,v~N(0,1) and are independent,
# it can be rewritten (taking symmetry into account) as:
# P = 1-4\int_0^{7/2}\int_{0}^{3+0.2*u^2}\phi(u)\phi(v)dvdu
# Maple gives P=0.2222795066194439887212863444e-2
P = 0.2222795066194439887212863444e-2
print("(Maple)                   P=", P)
print("beta=", -ot.DistFunc.qNormal(P))
lower = ot.SymbolicFunction("u", "0")
upper = ot.SymbolicFunction("u", "3+0.2*u^2")


def kernel(X):
    return [ot.Normal(2).computePDF(X)]


part_of_p = ot.IteratedQuadrature().integrate(
    ot.PythonFunction(2, 1, kernel), 0, 7 / 2, [lower], [upper]
)[0]

P = 1 - 4 * part_of_p
print("(Iterated quadrature)     P=", P)
# The innermost integral has a closed-form:
# P = 1-4\int_{0}^{7/2}(Phi(3+0.2*u^2)-1/2)\phi(u)du


def f(x):
    u = x[0]
    pnormal = ot.DistFunc.pNormal(3 + 0.2 * u ** 2) - 0.5
    return [pnormal * exp(-(u ** 2) / 2) * ot.SpecFunc.ISQRT2PI]


part_of_p = ot.GaussKronrod().integrate(
    ot.PythonFunction(1, 1, f), ot.Interval(0, 7 / 2)
)[0]

P = 1 - 4 * part_of_p
print("(Gauss Kronrod)           P=", P)
