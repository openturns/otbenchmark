"""
Benchmark sensitivity analysis methods
======================================
"""

# %%
import openturns as ot
import otbenchmark as otb

# %%
# When we estimate Sobol' indices, we may encounter the following warning messages:
# ```
# WRN - The estimated first order Sobol index (2) is greater than its total order index ...
# WRN - The estimated total order Sobol index (2) is lesser than first order index ...
# ```
# Lots of these messages are printed in the current Notebook. This is why we disable them with:
ot.Log.Show(ot.Log.NONE)

# %%
# Use Borgonovo problem
problem = otb.BorgonovoSensitivity()
distribution = problem.getInputDistribution()
model = problem.getFunction()

# %%
# Exact first and total order
exactFirstOrder = problem.getFirstOrderIndices()
exactTotalOrder = problem.getTotalOrderIndices()

# %%
# Saltelli estimator with Monte-Carlo sample
# ------------------------------------------

# %%
sampleSize = 10000

# %%
inputDesign = ot.SobolIndicesExperiment(distribution, sampleSize).generate()
outputDesign = model(inputDesign)

# %%
# Compute first order indices using the Saltelli estimator
sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(
    inputDesign, outputDesign, sampleSize
)
computedFirstOrder = sensitivityAnalysis.getFirstOrderIndices()
computedTotalOrder = sensitivityAnalysis.getTotalOrderIndices()

# %%
# Compare with exact results
print(f"Sample size : {sampleSize}")
# First order
print(f"Computed first order = {computedFirstOrder}")
print(f"Exact first order = {exactFirstOrder}")
# Total order
print(f"Computed total order = {computedTotalOrder}")
print(f"Exact total order = {exactTotalOrder}")

# %%
# Saltelli estimator with Quasi Monte-Carlo sample
# ------------------------------------------------

# %%
sampleSize = 500

# %%
dimension = distribution.getDimension()
sequence = ot.SobolSequence(dimension)
restart = True
experiment = ot.LowDiscrepancyExperiment(sequence, distribution, sampleSize, restart)

# %%
inputDesign = ot.SobolIndicesExperiment(experiment).generate()
outputDesign = model(inputDesign)

# %%
# Compute first order indices using the Saltelli estimator
sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(
    inputDesign, outputDesign, sampleSize
)
first_order = sensitivityAnalysis.getFirstOrderIndices()
total_order = sensitivityAnalysis.getTotalOrderIndices()

# %%
# Compare with exact results
print(f"Sample size : {sampleSize}")
# First order
print(f"Computed first order = {computedFirstOrder}")
print(f"Exact first order = {exactFirstOrder}")
# Total order
print(f"Computed total order = {computedTotalOrder}")
print(f"Exact total order = {exactTotalOrder}")

# %%
# Loop over the estimators
# ------------------------

# %%
print("Available estimators:")
estimators_list = otb.SensitivityBenchmarkMetaAlgorithm.GetEstimators()
for sobolAlgorithm in estimators_list:
    name = sobolAlgorithm.getClassName()
    print(" - ", name)

# %%
metaSAAlgorithm = otb.SensitivityBenchmarkMetaAlgorithm(problem)

# %%
print("Monte-Carlo sampling")
for sobolAlgorithm in estimators_list:
    (
        computedFirstOrder,
        computedTotalOrder,
    ) = metaSAAlgorithm.runSamplingEstimator(sampleSize)
    name = sobolAlgorithm.getClassName()
    print(name)
    print("    S = ", computedFirstOrder)
    print("    T = ", computedTotalOrder)

# %%
print("Quasi Monte-Carlo sampling")
for estimator in ["Saltelli", "Martinez", "Jansen", "MauntzKucherenko"]:
    (
        computedFirstOrder,
        computedTotalOrder,
    ) = metaSAAlgorithm.runSamplingEstimator(
        sampleSize, estimator=estimator, samplingMethod="QMC"
    )
    name = sobolAlgorithm.getClassName()
    print(name)
    print(f"    S = {computedFirstOrder}")
    print(f"    T = {computedTotalOrder}")

# %%
print("Polynomial chaos")
sampleSize = 500
(
    computedFirstOrder,
    computedTotalOrder,
) = metaSAAlgorithm.runPolynomialChaosEstimator(
    sampleSizeTrain=sampleSize,
    sampleSizeTest=2,
    totalDegree=5,
    hyperbolicQuasiNorm=0.5,
)
print(f"    S = {computedFirstOrder}")
print(f"    T = {computedTotalOrder}")

# %%
# Define the metric
# -----------------

# %%
# We consider the following accuracy metrics:
#
# * the vector or log relative errors for a given index (first order or total order),
# * the mean log relative error, as the mean of the LRE vector (first order or total order),
# * the average mean log relative error, as the mean of the first and total order mean log relative error.
#
# Larger LRE values are prefered.
#
# The first order (resp. total order) mean LRE represents the mean number of digits for all components
# of the first order indices (resp. total order indices).
# The average mean LRE represents the mean LRE for both first and total order indices.

# %%
S_LRE = ot.Point(dimension)
T_LRE = ot.Point(dimension)
for i in range(dimension):
    S_LRE[i] = otb.ComputeLogRelativeError(
        computedFirstOrder[i], exactFirstOrder[i]
    )
    T_LRE[i] = otb.ComputeLogRelativeError(
        computedTotalOrder[i], exactTotalOrder[i]
    )

# %%
print(f"LRE S = {S_LRE}")
print(f"LRE T = {T_LRE}")

# %%
mean_LRE_S = sum(S_LRE) / dimension
mean_LRE_T = sum(T_LRE) / dimension
mean_LRE = (mean_LRE_S + mean_LRE_T) / 2.0
print(f"Mean LRE S = {mean_LRE_S:.2f}")
print(f"Mean LRE T = {mean_LRE_T:.2f}")
print(f"Mean LRE = {mean_LRE:.2f}")

# %%
# The digit per point ratio measure the number of digits relatively to the sample size. A greater value is prefered.
digitPerPointRatio = mean_LRE / sampleSize
print(f"Digit / point = {digitPerPointRatio:.3e}")
