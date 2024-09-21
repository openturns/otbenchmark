#!/usr/bin/env python3
"""
Generate reference Morris Sobol' parameters.
"""

import openturns as ot

ot.RandomGenerator.SetSeed(0)
b0 = ot.DistFunc.rNormal()
alpha = ot.DistFunc.rNormal(10)
beta = ot.DistFunc.rNormal(6 * 14)
gamma = ot.DistFunc.rNormal(20 * 14)


def get_string(point, float_format="%.4f"):
    string_list = [float_format % (point[i]) for i in range(point.getDimension())]
    string_body = ",".join(string_list)
    full_string = "[" + string_body + "]"
    return full_string


print("b0=%.17f" % (b0))
print("alpha")
print(get_string(alpha, "%.8f"))
print("beta")
print(get_string(beta, "%.2f"))
print("gamma")
print(get_string(gamma, "%.1f"))
