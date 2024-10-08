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
exact_first_order = problem.getFirstOrderIndices()
exact_total_order = problem.getTotalOrderIndices()

# %%
# Saltelli estimator with Monte-Carlo sample
# ------------------------------------------

# %%
sample_size = 10000

# %%
inputDesign = ot.SobolIndicesExperiment(distribution, sample_size).generate()
outputDesign = model(inputDesign)

# %%
# Compute first order indices using the Saltelli estimator
sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(
    inputDesign, outputDesign, sample_size
)
computed_first_order = sensitivityAnalysis.getFirstOrderIndices()
computed_total_order = sensitivityAnalysis.getTotalOrderIndices()

# %%
# Compare with exact results
print("Sample size : ", sample_size)
# First order
print("Computed first order = ", computed_first_order)
print("Exact first order = ", exact_first_order)
# Total order
print("Computed total order = ", computed_total_order)
print("Exact total order = ", exact_total_order)

# %%
# Saltelli estimator with Quasi Monte-Carlo sample
# ------------------------------------------------

# %%
sample_size = 500

# %%
dimension = distribution.getDimension()
sequence = ot.SobolSequence(dimension)
restart = True
experiment = ot.LowDiscrepancyExperiment(sequence, distribution, sample_size, restart)

# %%
inputDesign = ot.SobolIndicesExperiment(experiment).generate()
outputDesign = model(inputDesign)

# %%
# Compute first order indices using the Saltelli estimator
sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(
    inputDesign, outputDesign, sample_size
)
first_order = sensitivityAnalysis.getFirstOrderIndices()
total_order = sensitivityAnalysis.getTotalOrderIndices()

# %%
# Compare with exact results
print("Sample size : ", sample_size)
# First order
print("Computed first order = ", computed_first_order)
print("Exact first order = ", exact_first_order)
# Total order
print("Computed total order = ", computed_total_order)
print("Exact total order = ", exact_total_order)

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
        computed_first_order,
        computed_total_order,
    ) = metaSAAlgorithm.runSamplingEstimator(sample_size)
    name = sobolAlgorithm.getClassName()
    print(name)
    print("    S = ", computed_first_order)
    print("    T = ", computed_total_order)

# %%
print("Quasi Monte-Carlo sampling")
for estimator in ["Saltelli", "Martinez", "Jansen", "MauntzKucherenko"]:
    (
        computed_first_order,
        computed_total_order,
    ) = metaSAAlgorithm.runSamplingEstimator(
        sample_size, estimator=estimator, sampling_method="QMC"
    )
    name = sobolAlgorithm.getClassName()
    print(name)
    print("    S = ", computed_first_order)
    print("    T = ", computed_total_order)

# %%
print("Polynomial chaos")
sample_size = 500
(
    computed_first_order,
    computed_total_order,
) = metaSAAlgorithm.runPolynomialChaosEstimator(
    sample_size_train=sample_size,
    sample_size_test=2,
    total_degree=5,
    hyperbolic_quasinorm=0.5,
)
print("    S = ", computed_first_order)
print("    T = ", computed_total_order)

# %%
# Define the metric
# -----------------

# %%
# We consider the following accuracy metrics:
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
        computed_first_order[i], exact_first_order[i]
    )
    T_LRE[i] = otb.ComputeLogRelativeError(
        computed_total_order[i], exact_total_order[i]
    )

# %%
print("LRE S = ", S_LRE)
print("LRE T = ", T_LRE)

# %%
mean_LRE_S = sum(S_LRE) / dimension
mean_LRE_T = sum(T_LRE) / dimension
mean_LRE = (mean_LRE_S + mean_LRE_T) / 2.0
print("Mean LRE S = %.2f" % (mean_LRE_S))
print("Mean LRE T = %.2f" % (mean_LRE_T))
print("Mean LRE = %.2f" % (mean_LRE))

# %%
# The digit per point ratio measure the number of digits relatively to the sample size. A greater value is prefered.
digit_per_point_ratio = mean_LRE / sample_size
print("Digit / point = %.3e" % (digit_per_point_ratio))
