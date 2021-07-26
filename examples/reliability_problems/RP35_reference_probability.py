#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author : Régis Lebrun, Feb 2021.

The reference value 0.00354 should be replaced by 0.00347894632
as shown by the following script.

The output is:

(Maple)               P= 0.00347894632
(Iterated quadrature) P= 0.003478946320122356
(Gauss Kronrod)       P= 0.003478946320929932
"""


import openturns as ot
from math import exp

ot.ResourceMap.SetAsScalar("GaussKronrod-MaximumError", 1.0e-15)
ot.ResourceMap.SetAsUnsignedInteger("GaussKronrod-MaximumSubIntervals", 4096)
ot.ResourceMap.SetAsScalar("IteratedQuadrature-MaximumError", 1.0e-8)
ot.ResourceMap.SetAsUnsignedInteger("IteratedQuadrature-MaximumSubIntervals", 256)

# P = P(min(2-x2+exp(-0.1*x1^2)+(0.2*x1)^4,4.5-x1*x2)<0)
# It can be rewritten as:
# P = P(A or B) = 1 - P(Ac and Bc)
# where A = 2-x2+exp(-0.1*x1^2)+(0.2*x1)^4<0, B = 4.5-x1*x2<0
#       Ac= 2-x2+exp(-0.1*x1^2)+(0.2*x1)^4>0, Bc= 4.5-x1*x2>0
# So it reduces to compute P'=P(Ac and Bc):
# P'=\int_{-\infty}^0\int_{4.5/x1}^{2+exp(-0.1*x1^2)+(0.2*x1)^4}phi(x1)phi(x2)dx1dx2+
#    \int_0^{x1_0}\int_{-\infty}^{2+exp(-0.1*x1^2)+(0.2*x1)^4}phi(x1)phi(x2)dx1dx2
# +
#    \int_{x1_0}^{+\infty}\int_{-\infty}^{4.5/x1}phi(x1)phi(x2)dx1dx2
# where x1_0 solves 2+exp(-0.1*x1^2)+(0.2*x1)^4=4.5/x1
# i.e. x1_0~1.61838417653828982908750781436
# Maple gives P=0.00347894632
print("(Maple)               P=", 0.00347894632)
lower = ot.SymbolicFunction("x1", "4.5/x1")
upper = ot.SymbolicFunction("x1", "2+exp(-0.1*x1^2)+(0.2*x1)^4")
x1_0 = 1.61838417653828982908750781436


def kernel(X):
    return [ot.Normal(2).computePDF(X)]


p_part1 = ot.IteratedQuadrature().integrate(
    ot.PythonFunction(2, 1, kernel), -8.5, 0.0, [lower], [upper]
)[0]
p_part2 = ot.IteratedQuadrature().integrate(
    ot.PythonFunction(2, 1, kernel),
    0.0,
    x1_0,
    [ot.SymbolicFunction("x1", "-8.5")],
    [upper],
)[0]
p_part3 = ot.IteratedQuadrature().integrate(
    ot.PythonFunction(2, 1, kernel),
    x1_0,
    8.5,
    [ot.SymbolicFunction("x1", "-8.5")],
    [lower],
)[0]
Pp = p_part1 + p_part2 + p_part3
print("(Iterated quadrature) P=", 1 - Pp)
# We can also rewrite the 2D integrals into 1D integrals
# P = \int_{x1_0}^{X1_1}(Phi(16*x1-32)-Phi(2+x1^2/8))\phi(x1)dx1


def f1(x):
    pnormal1 = ot.DistFunc.pNormal(upper(x)[0])
    pnormal2 = ot.DistFunc.pNormal(lower(x)[0])
    return [(pnormal1 - pnormal2) * exp(-x[0] ** 2 / 2) * ot.SpecFunc.ISQRT2PI]


def f2(x):
    pnormal = ot.DistFunc.pNormal(upper(x)[0])
    return [pnormal * exp(-x[0] ** 2 / 2) * ot.SpecFunc.ISQRT2PI]


def f3(x):
    pnormal = ot.DistFunc.pNormal(lower(x)[0])
    return [pnormal * exp(-x[0] ** 2 / 2) * ot.SpecFunc.ISQRT2PI]


p1 = ot.GaussKronrod().integrate(ot.PythonFunction(1, 1, f1), ot.Interval(-8.5, 0.0))[0]
p2 = ot.GaussKronrod().integrate(ot.PythonFunction(1, 1, f2), ot.Interval(0.0, x1_0))[0]
p3 = ot.GaussKronrod().integrate(ot.PythonFunction(1, 1, f3), ot.Interval(x1_0, 8.5))[0]
Pp = p1 + p2 + p3
print("(Gauss Kronrod)       P=", 1 - Pp)
