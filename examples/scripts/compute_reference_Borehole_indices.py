#!/usr/bin/env python3
"""
Compute reference Borehole Sobol' indices.
"""

import otbenchmark as otb

print("Get Borehole S.A. problem")
problem = otb.BoreholeSensitivity()
print(problem)
sample_size_train = 1000
sample_size_test = 1000
total_degree = 6
hyperbolic_quasinorm = 0.5  # the q-quasi-norm parameter
sparse_sa = otb.SparsePolynomialChaosSensitivityAnalysis(
    problem,
    sampleSizeTrain=sample_size_train,
    sampleSizeTest=sample_size_test,
    totalDegree=total_degree,
    hyperbolicQuasiNorm=hyperbolic_quasinorm,
)
result = sparse_sa.run(True)


def get_string(point, string_format="%.2f"):
    point_string = [string_format % (point[i]) for i in range(point.getDimension())]
    joined = ",".join(point_string)
    full_string = "[" + joined + "]"
    return full_string


first_order_string = get_string(result.first_order_indices)
print("First order indices")
print(first_order_string)
total_order_string = get_string(result.total_order_indices)
print("Total order indices")
print(total_order_string)
