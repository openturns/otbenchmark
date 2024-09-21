#!/usr/bin/env python3
"""
Compute reference Flooding Sobol' indices.
"""

import otbenchmark as otb

print("Get Flooding S.A. problem")
problem = otb.FloodingSensitivity()
print(problem)
sample_size_train = 1000
sample_size_test = 1000
total_degree = 8
hyperbolic_quasinorm = 0.5  # the q-quasi-norm parameter
sparse_sa = otb.SparsePolynomialChaosSensitivityAnalysis(
    problem,
    sample_size_train=sample_size_train,
    sample_size_test=sample_size_test,
    total_degree=total_degree,
    hyperbolic_quasinorm=hyperbolic_quasinorm,
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
