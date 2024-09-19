"""
Convergence of Monte-Carlo to estimate the probability in a reliability problem
===============================================================================
"""

# %%
# The goal of this document is to present the convergence of the Monte-Carlo algorithm
# to the exact probability when the sample size increases.
# This convergence is expressed in terms of absolute error.
# We show that the rate of convergence is :math:`O(\sqrt{n})`,
# where :math:`n` is the sample size.

# %%
import openturns as ot
import openturns.viewer as otv
import numpy as np
import otbenchmark as otb
import time

# %%
problem = otb.RminusSReliability()
print(problem)


def ComputeProbabilityFromMonteCarlo(
    problem, coefficientOfVariation=0.1, maximumOuterSampling=1000, blockSize=2
):
    event = problem.getEvent()
    g = event.getFunction()
    # Create the Monte-Carlo algorithm
    algoProb = ot.ProbabilitySimulationAlgorithm(event)
    algoProb.setMaximumOuterSampling(maximumOuterSampling)
    algoProb.setBlockSize(blockSize)
    algoProb.setMaximumCoefficientOfVariation(coefficientOfVariation)
    initialNumberOfFunctionEvaluations = g.getEvaluationCallsNumber()
    algoProb.run()
    # Get the results
    resultAlgo = algoProb.getResult()
    numberOfFunctionEvaluations = (
        g.getEvaluationCallsNumber() - initialNumberOfFunctionEvaluations
    )
    pf = resultAlgo.getProbabilityEstimate()
    level = 0.95
    c95 = resultAlgo.getConfidenceLength(level)
    pmin = pf - 0.5 * c95
    pmax = pf + 0.5 * c95
    print(
        "Number of function calls = %d" % (numberOfFunctionEvaluations),
        ", Pf = %.4f" % (pf),
        ", %.1f %% confidence interval :[%.4f,%.4f] " % (level * 100, pmin, pmax),
    )
    absoluteError = abs(pf - problem.getProbability())
    result = {
        "numberOfFunctionEvaluations": numberOfFunctionEvaluations,
        "pf": pf,
        "pmin": pmin,
        "pmax": pmax,
        "absoluteError": absoluteError,
    }
    return result


# %%
result = ComputeProbabilityFromMonteCarlo(problem)

# %%
numberOfPoints = 15  # Number of atomic experiments
numberOfRepetitions = 10  # Number of repetitions of each experiment
sampleSizeAbsoluteErrorTable = ot.Sample(numberOfPoints * numberOfRepetitions, 2)
sampleSizeAbsoluteErrorTable.setDescription(["Sample size", "Absolute error"])

# %%
cov = 0.0
startTime = time.time()

# %%
maximumOuterSampling = 1
index = 0
for i in range(numberOfPoints):
    maximumOuterSampling *= 2
    for j in range(numberOfRepetitions):
        result = ComputeProbabilityFromMonteCarlo(
            problem,
            coefficientOfVariation=cov,
            maximumOuterSampling=maximumOuterSampling,
        )
        sampleSizeAbsoluteErrorTable[index, 0] = result["numberOfFunctionEvaluations"]
        sampleSizeAbsoluteErrorTable[index, 1] = result["absoluteError"]
        index += 1

# %%
elapsedTime = time.time() - startTime
print("Elapsed = %.2f (s)" % (elapsedTime))

# %%
sampleSizeArray = [int(n) for n in np.logspace(0.0, 5.0)]
expectedConvergence = [1.0 / np.sqrt(n) for n in sampleSizeArray]

# %%
title = "Convergence of Monte-Carlo method - problem = %s" % (problem.getName())
graph = ot.Graph(title, "Sample size", "Absolute error", True, "topright")
curve = ot.Cloud(sampleSizeAbsoluteErrorTable, "blue", "fsquare", "")
curve.setLegend("Monte-Carlo")
graph.add(curve)
curve = ot.Curve(sampleSizeArray, expectedConvergence)
curve.setLegend(r"$1/\sqrt{n}$")
graph.add(curve)
graph.setLogScale(ot.GraphImplementation.LOGXY)
graph.setColors(["dodgerblue3", "darkorange1"])
_ = otv.View(graph)

# %%
otv.View.ShowAll()
