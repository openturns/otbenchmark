#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author : Régis Lebrun, Feb 2021.

The reference value 0.0107 should be replaced by 0.00981929872154689
as shown by the following script.

The output is:

(Maple)                   P= 0.00981929872154689
(Distribution arithmetic) P= 0.009819298721558622
(Iterated quadrature)     P= 0.00981929873302821
(Gauss Kronrod)           P= 0.009819298721546894
"""
import openturns as ot
from math import exp

# P = P(3-x1*x2<0)
# It can be rewritten (taking symmetry into account) as:
# P = 2\int_0^{\infty}\int_{3/x1}^{\infty}\phi(x1)\phi(x2)dx2dx1
# Maple gives P=0.981929872154689055665574917800e-2
print("(Maple)                   P=", 0.981929872154689055665574917800e-2)
# This time we get something meaningfull using distribution's arithmetic
P = (ot.Normal() * ot.Normal()).computeComplementaryCDF(3.0)
print("(Distribution arithmetic) P=", P)
lower = ot.SymbolicFunction("x1", "3/x1")
upper = ot.SymbolicFunction("x1", "8.5")


def kernel(X):
    return [ot.Normal(2).computePDF(X)]


half_p = ot.IteratedQuadrature().integrate(
    ot.PythonFunction(2, 1, kernel), 0, 8.5, [lower], [upper]
)[0]
P = 2 * half_p
print("(Iterated quadrature)     P=", P)
# The innermost integral has a closed-form:
# P = 2\int_{0}^{\infty}1-Phi(3/x1)\phi(x1)dx1


def f(x):
    x1 = x[0]
    pnormal = ot.DistFunc.pNormal(3 / x1, True)
    return [pnormal * exp(-(x1 ** 2) / 2) * ot.SpecFunc.ISQRT2PI]


P = 2 * ot.GaussKronrod().integrate(ot.PythonFunction(1, 1, f), ot.Interval(0, 8.5))[0]
print("(Gauss Kronrod)           P=", P)
