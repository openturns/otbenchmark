"""
Benchmark the reliability solvers on the problems
=================================================
"""

# %%
# In this example, we show how to run all the methods on all the problems and get the computed probability.

# %%
import openturns as ot
import numpy as np
import otbenchmark as otb
import pandas as pd
from tqdm import tqdm

# %%
ot.Log.Show(ot.Log.NONE)

# %%
# We import the list of reliability problems.
benchmarkProblemList = otb.ReliabilityBenchmarkProblemList()
numberOfProblems = len(benchmarkProblemList)
numberOfProblems

# %%
# For each problem in the benchmark, print the problem name and the exact failure probability.
for i in range(numberOfProblems):
    problem = benchmarkProblemList[i]
    name = problem.getName()
    pf = problem.getProbability()
    print("#", i, " : ", name, ", exact PF : ", pf)

# %%
# Run several algorithms on a single problem
# ------------------------------------------

# %%
# We want to run several algorithms on a single problem.
# We set the parameters of the algorithms and run them on a single problem.
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
i = 3
problem = benchmarkProblemList[i]
metaAlgorithm = otb.ReliabilityBenchmarkMetaAlgorithm(problem)

# %%
# We try the FORM algorithm.
benchmarkFORM = metaAlgorithm.runFORM(nearestPointAlgorithm)
s1 = benchmarkFORM.summary()
print(s1)

# %%
# Then the SORM algorithm.
benchmarkSORM = metaAlgorithm.runSORM(nearestPointAlgorithm)
s2 = benchmarkSORM.summary()
print(s2)

# %%
benchmarkMC = metaAlgorithm.runMonteCarlo(
    maximumOuterSampling=1000000, coefficientOfVariation=0.1, blockSize=1,
)
s3 = benchmarkMC.summary()
print(s3)

# %%
benchmarkFORMIS = metaAlgorithm.runFORMImportanceSampling(
    nearestPointAlgorithm,
    maximumOuterSampling=1000,
    coefficientOfVariation=0.1,
    blockSize=1,
)
s4 = benchmarkFORMIS.summary()
print(s4)

# %%
benchmarkSS = metaAlgorithm.runSubsetSampling(
    maximumOuterSampling=5000, coefficientOfVariation=0.1, blockSize=1,
)
s5 = benchmarkSS.summary()
print(s5)

# %%
# Run all algorithms on all problems and produce a single result table
# --------------------------------------------------------------------
#
# For several algorithms and all the reliability problems, we want to estimate the failure probability and compare them.

# %%
# We create a list of problem names.
problem_names = []
for i in range(numberOfProblems):
    problem = benchmarkProblemList[i]
    name = problem.getName()
    problem_names.append(name)


# %%
metrics = [
    "Exact",
    "FORM",
    "SORM",
    "Monte Carlo",
    "FORM-IS",
    "Subset",
]
results = np.zeros((numberOfProblems, len(metrics)))
maximumOuterSampling = 10 ** 2
blockSize = 10 ** 2
coefficientOfVariation = 0.0

for i in tqdm(range(numberOfProblems)):
    problem = benchmarkProblemList[i]
    results[i][0] = problem.getProbability()
    metaAlgorithm = otb.ReliabilityBenchmarkMetaAlgorithm(problem)
    benchmarkResult = metaAlgorithm.runFORM(nearestPointAlgorithm)
    results[i][1] = benchmarkResult.computedProbability
    benchmarkResult = metaAlgorithm.runSORM(nearestPointAlgorithm)
    results[i][2] = benchmarkResult.computedProbability
    benchmarkResult = metaAlgorithm.runMonteCarlo(
        maximumOuterSampling=maximumOuterSampling,
        coefficientOfVariation=coefficientOfVariation,
        blockSize=blockSize,
    )
    results[i][3] = benchmarkResult.computedProbability
    benchmarkResult = metaAlgorithm.runFORMImportanceSampling(
        nearestPointAlgorithm,
        maximumOuterSampling=maximumOuterSampling,
        coefficientOfVariation=coefficientOfVariation,
        blockSize=blockSize,
    )
    results[i][4] = benchmarkResult.computedProbability
    benchmarkResult = metaAlgorithm.runSubsetSampling(
        maximumOuterSampling=maximumOuterSampling,
        coefficientOfVariation=coefficientOfVariation,
        blockSize=blockSize,
    )
    results[i][5] = benchmarkResult.computedProbability

df = pd.DataFrame(results, index=problem_names, columns=metrics)
# df.to_csv("reliability_benchmark_table-output.csv")
df

# %%
# Run several algorithms on all problems and get detailed statistics
# ------------------------------------------------------------------
#
# Run several algorithms on all reliability benchmark problems: print statistics on each problem.

# %%


def FormatRow(benchmarkResult):
    """Format a single row of the benchmark table"""
    result = [
        benchmarkResult.exactProbability,
        benchmarkResult.computedProbability,
        benchmarkResult.absoluteError,
        benchmarkResult.numberOfCorrectDigits,
        benchmarkResult.numberOfFunctionEvaluations,
        benchmarkResult.numberOfDigitsPerEvaluation,
    ]
    return result


# %%
method_names = ["Monte-Carlo", "FORM", "SORM", "FORM-IS", "SUBSET"]

maximumOuterSampling = 10 ** 2
blockSize = 10 ** 2
coefficientOfVariation = 0.0

result = dict()
for i in range(numberOfProblems):
    problem = benchmarkProblemList[i]
    name = problem_names[i]
    exact_pf_name = "%10s" % ("Exact PF " + name[0:10])
    metrics = [
        exact_pf_name,
        "Estimated PF",
        "Absolute Error",
        "Correct Digits",
        "Function Calls",
        "Digits / Evaluation",
    ]
    results = np.zeros((len(method_names), len(metrics)))
    metaAlgorithm = otb.ReliabilityBenchmarkMetaAlgorithm(problem)
    # Monte-Carlo
    benchmarkResult = metaAlgorithm.runMonteCarlo(
        maximumOuterSampling=maximumOuterSampling,
        coefficientOfVariation=coefficientOfVariation,
        blockSize=blockSize,
    )
    results[0, :] = FormatRow(benchmarkResult)
    # FORM
    benchmarkResult = metaAlgorithm.runFORM(nearestPointAlgorithm)
    results[1, :] = FormatRow(benchmarkResult)
    # SORM
    benchmarkResult = metaAlgorithm.runSORM(nearestPointAlgorithm)
    results[2, :] = FormatRow(benchmarkResult)
    # FORM-IS
    benchmarkResult = metaAlgorithm.runFORMImportanceSampling(
        nearestPointAlgorithm,
        maximumOuterSampling=maximumOuterSampling,
        coefficientOfVariation=coefficientOfVariation,
        blockSize=blockSize,
    )
    results[3, :] = FormatRow(benchmarkResult)
    # Subset
    benchmarkResult = metaAlgorithm.runSubsetSampling(
        maximumOuterSampling=maximumOuterSampling,
        coefficientOfVariation=coefficientOfVariation,
        blockSize=blockSize,
    )
    results[4, :] = FormatRow(benchmarkResult)
    # Gather statistics and print them
    df = pd.DataFrame(results, index=method_names, columns=metrics,)
    # Format the columns for readability
    s = df.style.format(
        {
            exact_pf_name: lambda x: "{:.3e}".format(x),
            "Estimated PF": lambda x: "{:.3e}".format(x),
            "Absolute Error": lambda x: "{:.3e}".format(x),
            "Correct Digits": lambda x: "{:.1f}".format(x),
            "Function Calls": lambda x: "{:d}".format(int(x)),
            "Digits / Evaluation": lambda x: "{:.1f}".format(x),
        }
    )
    result[name] = s

# %%
result["RP33"]

# %%
result["RP35"]
