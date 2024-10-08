"""
Convergence of estimators on Ishigami
=====================================
"""

# %%
# In this example, we present the convergence of the sensitivity indices of the Ishigami test function.
#
# We compare different estimators.
# * Sampling methods with different estimators: Saltelli, Mauntz-Kucherenko, Martinez, Jansen,
# * Sampling methods with different design of experiments: Monte-Carlo, LHS, Quasi-Monte-Carlo,
# * Polynomial chaos.
#

# %%
import openturns as ot
import otbenchmark as otb
import openturns.viewer as otv
import numpy as np


# %%
# When we estimate Sobol' indices, we may encounter the following warning messages:
# ```
# WRN - The estimated first order Sobol index (2) is greater than its total order index...
# WRN - The estimated total order Sobol index (2) is lesser than first order index ...
# ```
# Lots of these messages are printed in the current Notebook. This is why we disable them with:
ot.Log.Show(ot.Log.NONE)


# %%
problem = otb.IshigamiSensitivity()
print(problem)

# %%
distribution = problem.getInputDistribution()
model = problem.getFunction()

# %%
# Exact first and total order
exact_first_order = problem.getFirstOrderIndices()
print(exact_first_order)
exact_total_order = problem.getTotalOrderIndices()
print(exact_total_order)

# %%
# Perform sensitivity analysis
# ----------------------------

# %%
# Create X/Y data
ot.RandomGenerator.SetSeed(0)
size = 10000
inputDesign = ot.SobolIndicesExperiment(distribution, size).generate()
outputDesign = model(inputDesign)

# %%
# Compute first order indices using the Saltelli estimator
sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(inputDesign, outputDesign, size)
computed_first_order = sensitivityAnalysis.getFirstOrderIndices()
computed_total_order = sensitivityAnalysis.getTotalOrderIndices()

# %%
# Compare with exact results
print("Sample size : ", size)
# First order
# Compute absolute error (the LRE cannot be computed,
# because S can be zero)
print("Computed first order = ", computed_first_order)
print("Exact first order    = ", exact_first_order)
# Total order
print("Computed total order = ", computed_total_order)
print("Exact total order    = ", exact_total_order)

# %%
dimension = distribution.getDimension()

# %%
# Compute componentwise absolute error.
first_order_AE = ot.Point(np.abs(exact_first_order - computed_first_order))
total_order_AE = ot.Point(np.abs(exact_total_order - computed_total_order))

# %%
print("Absolute error")
for i in range(dimension):
    print(
        "AE(S%d) = %.4f, AE(T%d) = %.4f" % (i, first_order_AE[i], i, total_order_AE[i])
    )

# %%
metaSAAlgorithm = otb.SensitivityBenchmarkMetaAlgorithm(problem)
for estimator in ["Saltelli", "Martinez", "Jansen", "MauntzKucherenko", "Janon"]:
    print("Estimator:", estimator)
    benchmark = otb.SensitivityConvergence(
        problem,
        metaSAAlgorithm,
        numberOfRepetitions=4,
        maximum_elapsed_time=2.0,
        sample_size_initial=20,
        estimator=estimator,
    )
    grid = benchmark.plotConvergenceGrid(verbose=False)
    view = otv.View(grid)
    figure = view.getFigure()
    _ = figure.suptitle("%s, %s" % (problem.getName(), estimator))
    figure.set_figwidth(10.0)
    figure.set_figheight(5.0)
    figure.subplots_adjust(wspace=0.4, hspace=0.4)

# %%
benchmark = otb.SensitivityConvergence(
    problem,
    metaSAAlgorithm,
    numberOfRepetitions=4,
    maximum_elapsed_time=2.0,
    sample_size_initial=20,
    estimator="Saltelli",
    sampling_method="MonteCarlo",
)
graph = benchmark.plotConvergenceCurve()
_ = otv.View(graph)

# %%
grid = ot.GridLayout(1, 3)
maximum_absolute_error = 1.0
minimum_absolute_error = 1.0e-5
sampling_method_list = ["MonteCarlo", "LHS", "QMC"]
for sampling_method_index in range(3):
    sampling_method = sampling_method_list[sampling_method_index]
    benchmark = otb.SensitivityConvergence(
        problem,
        metaSAAlgorithm,
        numberOfRepetitions=4,
        maximum_elapsed_time=2.0,
        sample_size_initial=20,
        estimator="Saltelli",
        sampling_method=sampling_method,
    )
    graph = benchmark.plotConvergenceCurve()
    # Change bounding box
    box = graph.getBoundingBox()
    bound = box.getLowerBound()
    bound[1] = minimum_absolute_error
    box.setLowerBound(bound)
    bound = box.getUpperBound()
    bound[1] = maximum_absolute_error
    box.setUpperBound(bound)
    graph.setBoundingBox(box)
    grid.setGraph(0, sampling_method_index, graph)
_ = otv.View(grid)

# %%
# Use polynomial chaos.
benchmark = otb.SensitivityConvergence(
    problem,
    metaSAAlgorithm,
    numberOfExperiments=12,
    numberOfRepetitions=1,
    maximum_elapsed_time=5.0,
    sample_size_initial=20,
    use_sampling=False,
    total_degree=20,
    hyperbolic_quasinorm=1.0,
)
graph = benchmark.plotConvergenceCurve(verbose=True)
graph.setLegendPosition("bottomleft")
_ = otv.View(graph)

# %%
otv.View.ShowAll()
