"""
Benchmark on a given set of problems
====================================
"""

# %%
# In this example, we show how to make a loop over the problems in the benchmark.
# We also show how to run various reliability algorithms on a given problem so that
# we can score the methods using number of digits or performance.

# %%
import openturns as ot
import numpy as np
import otbenchmark as otb

# %%
# Browse the reliability problems
# -------------------------------

# %%
# We present the BBRC test cases using the otbenchmark module.
benchmarkProblemList = otb.ReliabilityBenchmarkProblemList()
numberOfProblems = len(benchmarkProblemList)
numberOfProblems


# %%
for i in range(numberOfProblems):
    problem = benchmarkProblemList[i]
    name = problem.getName()
    pf = problem.getProbability()
    event = problem.getEvent()
    antecedent = event.getAntecedent()
    distribution = antecedent.getDistribution()
    dimension = distribution.getDimension()
    print("#", i, ":", name, " : pf = ", pf, ", dimension=", dimension)


# %%
maximumEvaluationNumber = 1000
maximumAbsoluteError = 1.0e-3
maximumRelativeError = 1.0e-3
maximumResidualError = 1.0e-3
maximumConstraintError = 1.0e-3
nearestPointAlgorithm = ot.AbdoRackwitz()
nearestPointAlgorithm.setMaximumCallsNumber(maximumEvaluationNumber)
nearestPointAlgorithm.setMaximumAbsoluteError(maximumAbsoluteError)
nearestPointAlgorithm.setMaximumRelativeError(maximumRelativeError)
nearestPointAlgorithm.setMaximumResidualError(maximumResidualError)
nearestPointAlgorithm.setMaximumConstraintError(maximumConstraintError)

# %%
# The FORM method
# ---------------

# %%
problem = otb.ReliabilityProblem8()

# %%
metaAlgorithm = otb.ReliabilityBenchmarkMetaAlgorithm(problem)

# %%
benchmarkResult = metaAlgorithm.runFORM(nearestPointAlgorithm)
benchmarkResult.summary()

# %%
# The SORM method
# ---------------

# %%
benchmarkResult = metaAlgorithm.runSORM(nearestPointAlgorithm)
benchmarkResult.summary()

# %%
# The LHS method
# --------------

# %%
benchmarkResult = metaAlgorithm.runLHS(maximumOuterSampling=10000)
benchmarkResult.summary()

# %%
# The MonteCarloSampling method
# -----------------------------

# %%
benchmarkResult = metaAlgorithm.runMonteCarlo(maximumOuterSampling=10000)
benchmarkResult.summary()

# %%
# The FORM - Importance Sampling method
# -------------------------------------

# %%
benchmarkResult = metaAlgorithm.runFORMImportanceSampling(nearestPointAlgorithm)
benchmarkResult.summary()

# %%
# The Subset method
# -----------------

# %%
benchmarkResult = metaAlgorithm.runSubsetSampling()
benchmarkResult.summary()

# %%
# The following function computes the number of correct base-10 digits
# in the computed result compared to the exact result.
# The `CompareMethods` function takes as a parameter a problem
# and it returns the probabilities estimated by each method.
# In addition, it returns the performance of these methods.

# %%


def PrintResults(name, benchmarkResult):
    print("------------------------------------------------------------------")
    print(name)
    numberOfDigitsPerEvaluation = (
        benchmarkResult.numberOfCorrectDigits
        / benchmarkResult.numberOfFunctionEvaluations
    )
    print("Estimated probability:", benchmarkResult.computedProbability)
    print("Number of function calls:", benchmarkResult.numberOfFunctionEvaluations)
    print("Number of correct digits=%.1f" % (benchmarkResult.numberOfCorrectDigits))
    print(
        "Performance=%.2e (correct digits/evaluation)" % (numberOfDigitsPerEvaluation)
    )
    return [name, benchmarkResult.numberOfCorrectDigits, numberOfDigitsPerEvaluation]


# %%


def CompareMethods(problem, nearestPointAlgorithm, maximumOuterSampling=10000):
    """
    Runs various algorithms on a given problem.
    """
    summaryList = []
    pfReference = problem.getProbability()
    print("Exact probability:", pfReference)
    metaAlgorithm = otb.ReliabilityBenchmarkMetaAlgorithm(problem)
    # SubsetSampling
    benchmarkResult = metaAlgorithm.runSubsetSampling()
    summaryList.append(PrintResults("SubsetSampling", benchmarkResult))
    # FORM
    benchmarkResult = metaAlgorithm.runFORM(nearestPointAlgorithm)
    summaryList.append(PrintResults("FORM", benchmarkResult))
    # SORM
    benchmarkResult = metaAlgorithm.runSORM(nearestPointAlgorithm)
    summaryList.append(PrintResults("SORM", benchmarkResult))
    # FORM - ImportanceSampling
    benchmarkResult = metaAlgorithm.runFORMImportanceSampling(
        nearestPointAlgorithm, maximumOuterSampling=maximumOuterSampling
    )
    summaryList.append(PrintResults("FORM-IS", benchmarkResult))
    # MonteCarloSampling
    benchmarkResult = metaAlgorithm.runMonteCarlo(
        maximumOuterSampling=maximumOuterSampling
    )
    summaryList.append(PrintResults("MonteCarloSampling", benchmarkResult))
    # LHS
    benchmarkResult = metaAlgorithm.runLHS()
    summaryList.append(PrintResults("LHS", benchmarkResult))
    # Gather results
    numberOfMethods = len(summaryList)
    correctDigitsList = []
    performanceList = []
    algorithmNames = []
    for i in range(numberOfMethods):
        [name, numberOfCorrectDigits, numberOfDigitsPerEvaluation] = summaryList[i]
        algorithmNames.append(name)
        correctDigitsList.append(numberOfCorrectDigits)
        performanceList.append(numberOfDigitsPerEvaluation)
    print("------------------------------------------------------------------------")
    print("Scoring by number of correct digits")
    indices = np.argsort(correctDigitsList)
    rank = list(indices)
    for i in range(numberOfMethods):
        j = rank[i]
        print("%d : %s (%.1f)" % (j, algorithmNames[j], correctDigitsList[j]))
    print("------------------------------------------------------------------------")
    print("Scoring by performance (digits/evaluation)")
    indices = np.argsort(performanceList)
    rank = list(indices)
    for i in range(len(indices)):
        j = rank[i]
        print("%d : %s (%.1e)" % (j, algorithmNames[j], performanceList[j]))
    return correctDigitsList, performanceList


# %%
problem = otb.ReliabilityProblem8()
_ = CompareMethods(problem, nearestPointAlgorithm)

# %%
# Remarks
# -------
#
# * We note that the FORM and SORM methods are faster, but, they do not converge to the exact proba.
# * We also notice the effectiveness of the FORM-ImportanceSampling method (inexpensive method, and converges).
# * The convergence of the MonteCarlo method requires a large number of simulations.
# * SubsetSampling converges even if the probability is very low.
#
