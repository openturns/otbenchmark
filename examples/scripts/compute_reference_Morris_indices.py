#!/usr/bin/env python3
"""
Compute reference Morris Sobol' indices.

Compute Sobol' indices using PCE...
Generate train experiment, N=16384
Create polynomial chaos expansion..
> Sparse = False
> Total degree = 6
> Basis dimension = 6581
> Fit
> Number of selected coefficients: 6581
> Validation...
> Generate test experiment, N=16384
> Q2=99.47%
> Sensitivity Analysis...
Elapsed = 406.66 (s)

"""

# %%
import openturns as ot
import otbenchmark as otb
import time

# %%
# Set to fast mode for continuous integration testing
isFast = True  # Set to False to run with more samples and get more accurate indices

# %%
print("Get Morris S.A. problem")
problem = otb.MorrisSensitivity()
print(problem)

# %%
print("Compute Sobol' indices using PCE...")
t1 = time.time()
sampleSizeTrain = 2**10 if isFast else 2**16
sampleSizeTest = sampleSizeTrain
totalDegree = 2 if isFast else 6
hyperbolicQuasiNorm = 0.7  # the q-quasi-norm parameter
sparse_sa = otb.SparsePolynomialChaosSensitivityAnalysis(
    problem,
    sampleSizeTrain=sampleSizeTrain,
    sampleSizeTest=sampleSizeTest,
    totalDegree=totalDegree,
    hyperbolicQuasiNorm=hyperbolicQuasiNorm,
    sparse=False
)
result = sparse_sa.run(True)
t2 = time.time()
print(f"Elapsed = {t2 - t1:.2f} (s)")


# %%
def get_string(point, string_format="%.7f"):
    point_string = [string_format % (point[i]) for i in range(point.getDimension())]
    joined = ",".join(point_string)
    full_string = "[" + joined + "]"
    return full_string


# %%
first_order_string = get_string(result.firstOrderIndices)
print("First order indices")
print(first_order_string)
total_order_string = get_string(result.totalOrderIndices)
print("Total order indices")
print(total_order_string)


# %%
print("Compare reference to computed indices")
dimension = problem.getInputDistribution().getDimension()
reference_first_order = problem.getFirstOrderIndices()
reference_total_order = problem.getTotalOrderIndices()

# %%
def comparisonSample(point1, point2):
    dimension = point1.getDimension()
    sample = ot.Sample(dimension, 3)
    sample[:, 0] = ot.Sample.BuildFromPoint(point1)
    sample[:, 1] = ot.Sample.BuildFromPoint(point2)
    for i in range(dimension):
        sample[i, 2] = abs(point1[i] - point2[i])
    sample.setDescription(["Reference", "Computed", "Difference"])
    return sample

# %%
print("First order indices")
first_order_table = comparisonSample(reference_first_order, result.firstOrderIndices)
print(first_order_table)

# %%
print("Total order indices")
total_order_table = comparisonSample(reference_total_order, result.totalOrderIndices)
print(total_order_table)

# %%
