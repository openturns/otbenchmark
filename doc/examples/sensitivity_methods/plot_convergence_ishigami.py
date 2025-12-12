"""
Convergence of estimators on Ishigami
=====================================
"""

# %%
# In this example, we present the convergence of the sensitivity indices of the Ishigami test function.
#
# We compare different estimators.
#
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
maximumElapsedTime = 0.5

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
exactFirstOrder = problem.getFirstOrderIndices()
print(exactFirstOrder)
exactTotalOrder = problem.getTotalOrderIndices()
print(exactTotalOrder)

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
computedFirstOrder = sensitivityAnalysis.getFirstOrderIndices()
computedTotalOrder = sensitivityAnalysis.getTotalOrderIndices()

# %%
# Compare with exact results
print("Sample size : ", size)
# First order
# Compute absolute error (the LRE cannot be computed,
# because S can be zero)
print("Computed first order = ", computedFirstOrder)
print("Exact first order    = ", exactFirstOrder)
# Total order
print("Computed total order = ", computedTotalOrder)
print("Exact total order    = ", exactTotalOrder)

# %%
dimension = distribution.getDimension()

# %%
# Compute componentwise absolute error.
firstOrderAE = ot.Point(np.abs(exactFirstOrder - computedFirstOrder))
totalOrderAE = ot.Point(np.abs(exactTotalOrder - computedTotalOrder))

# %%
print("Absolute error")
for i in range(dimension):
    print(
        "AE(S%d) = %.4f, AE(T%d) = %.4f" % (i, firstOrderAE[i], i, totalOrderAE[i])
    )

# %%
metaSAAlgorithm = otb.SensitivityBenchmarkMetaAlgorithm(problem)

# %%
for estimator in ["Saltelli", "Martinez", "Jansen", "MauntzKucherenko", "Janon"]:
    print("Estimator:", estimator)
    benchmark = otb.SensitivityConvergence(
        problem,
        metaSAAlgorithm,
        numberOfRepetitions=4,
        maximumElapsedTime=maximumElapsedTime,
        sampleSizeInitial=20,
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
    maximumElapsedTime=maximumElapsedTime,
    sampleSizeInitial=20,
    estimator="Saltelli",
    samplingMethod="MonteCarlo",
)
graph = benchmark.plotConvergenceCurve()
graph.setLegendPosition("upper left")
graph.setLegendCorner((1.0, 1.0))
_ = otv.View(graph, figure_kw={"figsize": (4.0, 3.0)})

# %%
grid = ot.GridLayout(1, 3)
maximumAbsoluteError = 1.0
minimumAbsoluteError = 1.0e-5
samplingMethodList = ["MonteCarlo", "LHS", "QMC"]
estimator = "Saltelli"
for samplingMethodIndex, samplingMethod in enumerate(samplingMethodList):
    samplingMethod = samplingMethodList[samplingMethodIndex]
    benchmark = otb.SensitivityConvergence(
        problem,
        metaSAAlgorithm,
        numberOfRepetitions=4,
        maximumElapsedTime=maximumElapsedTime,
        sampleSizeInitial=20,
        estimator=estimator,
        samplingMethod=samplingMethod,
    )
    graph = benchmark.plotConvergenceCurve()
    # Change bounding box
    box = graph.getBoundingBox()
    bound = box.getLowerBound()
    bound[1] = minimumAbsoluteError
    box.setLowerBound(bound)
    bound = box.getUpperBound()
    bound[1] = maximumAbsoluteError
    box.setUpperBound(bound)
    graph.setBoundingBox(box)
    if samplingMethodIndex < len(samplingMethodList) - 1:
        graph.setLegends([""])
    else:
        graph.setLegendPosition("upper left")
        graph.setLegendCorner((1.0, 1.0))
    if samplingMethodIndex > 0:
        graph.setYTitle("")
    graph.setTitle(f"{samplingMethod}")
    grid.setGraph(0, samplingMethodIndex, graph)
grid.setTitle(f"Ishigami, {estimator}")
_ = otv.View(grid, figure_kw={"figsize": (8.0, 4.0)})

# %%
# Use polynomial chaos.
sparse = True  # Otherwise, the PCE estimator is too slow for this example.
benchmark = otb.SensitivityConvergence(
    problem,
    metaSAAlgorithm,
    numberOfExperiments=12,
    numberOfRepetitions=1,
    maximumElapsedTime=5.0,
    sampleSizeInitial=80,
    useSampling=False,
    totalDegree=8,
    hyperbolicQuasiNorm=1.0,
    sampleSizeFactor=1.5,
    sparse=sparse,
)
graph = benchmark.plotConvergenceCurve(verbose=True)
graph.setLegendPosition("upper left")
graph.setLogScale(ot.GraphImplementation.LOGX)
graph.setLegendCorner((1.0, 1.0))
_ = otv.View(graph, figure_kw={"figsize": (4.0, 3.0)})

# %%
otv.View.ShowAll()
