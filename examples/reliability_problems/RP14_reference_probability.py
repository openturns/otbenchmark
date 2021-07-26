#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author : Régis Lebrun, Feb 2021.

The reference value 0.00752 should be replaced by 0.0007728524
as shown by the following script.

The output is:

(Maple) P= 0.00077285
==================================================
N= 1 P(GL)= 0.0046117332535185514 t= 0.0001838207244873047 s
N= 1 P(F1)= 0.0046117332535185514 t= 0.00019025802612304688 s
N= 1 P(F2)= 0.0 t= 0.0001418590545654297 s
==================================================
N= 2 P(GL)= 6.1469744831223895e-12 t= 0.0002048015594482422 s
N= 2 P(F1)= 2.3315744240696198e-17 t= 0.00019240379333496094 s
N= 2 P(F2)= 0.0 t= 0.00017571449279785156 s
==================================================
N= 4 P(GL)= 3.531713743724772e-06 t= 0.000484466552734375 s
N= 4 P(F1)= 8.160768548080179e-07 t= 0.0004601478576660156 s
N= 4 P(F2)= 1.9769379048277337e-05 t= 0.0005035400390625 s
==================================================
N= 8 P(GL)= 0.0001093310896783891 t= 0.002862691879272461 s
N= 8 P(F1)= 7.826603445843518e-05 t= 0.0028426647186279297 s
N= 8 P(F2)= 0.0005615074648658518 t= 0.0028791427612304688 s
==================================================
N= 16 P(GL)= 0.0006402595632464924 t= 0.025142908096313477 s
N= 16 P(F1)= 0.0005936792238713716 t= 0.025747299194335938 s
N= 16 P(F2)= 0.0007298916235689975 t= 0.026662588119506836 s
==================================================
N= 32 P(GL)= 0.0007841959249039429 t= 0.28505635261535645 s
N= 32 P(F1)= 0.0007884918551235823 t= 0.28975486755371094 s
N= 32 P(F2)= 0.0007778170072135567 t= 0.2893202304840088 s
==================================================
N= 64 P(GL)= 0.000772444629858543 t= 3.791130542755127 s
N= 64 P(F1)= 0.0007724974177456858 t= 3.904017925262451 s
N= 64 P(F2)= 0.0007724626116772555 t= 3.913358211517334 s
==================================================
N= 128 P(GL)= 0.000772857042456145 t= 53.84338617324829 s
N= 128 P(F1)= 0.0007728504452350935 t= 56.009029150009155 s
N= 128 P(F2)= 0.00077284546574081 t= 52.465112924575806 s
==================================================
N= 256 P(GL)= 0.0007728528533694079 t= 801.527804851532 s
N= 256 P(F1)= 0.0007728529909717312 t= 800.2324950695038 s
N= 256 P(F2)= 0.0007728518709312712 t= 793.3074824810028 s
==================================================
N= 512 P(GL)= 0.000772852390199883 t= 12991.026317119598 s
N= 512 P(F1)= 0.0007728523594272409 t= 11992.123596668243 s
N= 512 P(F2)= 0.000772852418477453 t= 12013.319508552551 s

"""


import openturns as ot
from time import time

threshold = 0.0
a = 70.0
b = 80.0
mu2 = 39.0
sigma2 = 0.1
mu3 = 1500.0
sigma3 = 350.0
mu4 = 400.0
sigma4 = 0.1
mu5 = 250000.0
sigma5 = 35000.0
X1 = ot.Uniform(a, b)
X1.setDescription(["X1"])
X2 = ot.Normal(mu2, sigma2)
X2.setDescription(["X2"])
param3 = ot.GumbelMuSigma(mu3, sigma3)
X3 = ot.ParametrizedDistribution(param3)
X3.setDescription(["X3"])
X4 = ot.Normal(mu4, sigma4)
X4.setDescription(["X4"])
X5 = ot.Normal(mu5, sigma5)
X5.setDescription(["X5"])

ot.Log.Show(ot.Log.ALL)
# A first try is to use distribution arithmetic, which gives useless results
# print("Create G")
# t0 = time()
# G = X1 - 32 / (pi * X2**3) * (X3**2 * X4**2 / 16 + X5**2).sqrt()
# t1 = time()
# print("t=", t1 - t0, "s")
# print("Compute P")
# t0 = time()
# print(G.computeCDF(0.0))
# t1 = time()
# print("t=", t1 - t0, "s")

# The problem can be reformulated as a 4D integral:
# G < 0 <==>
# X1<8/(pi*x2**3)*sqrt(x3**2*x4**2+16*x5**2)
# =F_1(8/(pi*x2**3)*sqrt(x3**2*x4**2+16*x5**2))
# =0 if 8/(pi*x2**3)*sqrt(x3**2*x4**2+16*x5**2)<=70 i.e.
#     when x2>=[4/(35*pi)*sqrt(x3**2*x4**2+16*x5**2)]^{1/3}
# =1 if 8/(pi*x2**3)*sqrt(x3**2*x4**2+16*x5**2)>=80 i.e.
#     when x2<=[1/(10*pi)*sqrt(x3**2*x4**2+16*x5**2)]^{1/3}
# =4/(5*pi*x2**3)*sqrt(x3**2*x4**2+16*x5**2) else
# so integrating wrt x2 gives
# P = int_{-\infty}^{\infty}int_{-\infty}^{\infty}int_{-\infty}^{\infty}
# Using this, Maple is able to give a 4 figures value:
# P = 0.00077285
P = 0.00077285
print("(Maple) P=", P)
# Here we can use IteratedQuadrature with different underlying 1D algorithms
# We use a SymbolicFunction, much more efficient than a PythonFunction
Xreduced = ot.ComposedDistribution([X2, X3, X4, X5])

bet, gam = param3.getDistribution().getParameter()
formula = "max(0, min(1, 32/(pi_*x2^3)*sqrt(x3^2*x4^2/16+x5^2)/10 - 7))*"
formula += "exp(-0.5*((x2-39)^2/0.1^2+(x4-400)^2/0.1^2+(x5-250000)^2/35000^2))/"
formula += "((2*pi_)^(3/2)*0.1*0.1*35000)*exp(-(x3-"
formula += str(gam) + ") / " + str(bet) + "-exp(-(x3-" + str(gam)
formula += ") / " + str(bet) + ")) / " + str(bet)

fun = ot.SymbolicFunction(["x2", "x3", "x4", "x5"], [formula])

# The full loop takes a llllooonnnggg time to complete!
for N in range(1, 5):
    print("=" * 50)
    t0 = time()
    P = ot.IteratedQuadrature(ot.GaussLegendre([2 ** N])).integrate(
        fun, Xreduced.getRange()
    )[0]
    t1 = time()
    print("N=", 2 ** N, "P(GL)=", P, "t=", t1 - t0, "s")
    t0 = time()
    P = ot.IteratedQuadrature(
        ot.FejerAlgorithm([2 ** N], ot.FejerAlgorithm.FEJERTYPE1)
    ).integrate(fun, Xreduced.getRange())[0]
    t1 = time()
    print("N=", 2 ** N, "P(F1)=", P, "t=", t1 - t0, "s")
    t0 = time()
    P = ot.IteratedQuadrature(
        ot.FejerAlgorithm([2 ** N], ot.FejerAlgorithm.FEJERTYPE2)
    ).integrate(fun, Xreduced.getRange())[0]
    t1 = time()
    print("N=", 2 ** N, "P(F2)=", P, "t=", t1 - t0, "s")
