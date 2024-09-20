"""
Compute reference probabilities with Monte-Carlo
================================================
"""

# %%
# In this example, we perform a reliability benchmark based on a large Monte-Carlo sample.
# In order to limit the elapsed time, we consider a limited elapsed time for each problem.
# In order to get the best possible accuracy within this time limit, we set the coefficient of variation to zero.

# %%
import otbenchmark as otb
import pandas as pd
import numpy as np
from tqdm import tqdm
import time


# %%
problemslist = otb.ReliabilityBenchmarkProblemList()
numberOfProblems = len(problemslist)
numberOfProblems


# %%
coefficientOfVariation = 0.0
maximumOuterSampling = 10 ** 4  # 10 ** 6 for real
blockSize = 10 ** 0  # 10 ** 4 for real simulations
blockSize

# %%
confidenceLevel = 0.95
maximumDurationSeconds = 5 * 60.0

# %%
totalDurationMinutes = numberOfProblems * maximumDurationSeconds / 60.0
totalDurationMinutes

# %%
model_names = [problemslist[i].getName() for i in range(numberOfProblems)]
metrics = ["PF", "N. function calls", "PMin", "PMax", "C.O.V.", "Digits", "Time (s)"]
resultArray = np.zeros((numberOfProblems, len(metrics)))
for i in tqdm(range(numberOfProblems)):
    startTime = time.time()
    problem = problemslist[i]
    name = problem.getName()
    event = problem.getEvent()
    g = event.getFunction()
    factory = otb.ProbabilitySimulationAlgorithmFactory()
    algo = factory.buildMonteCarlo(problem)
    algo.setMaximumOuterSampling(maximumOuterSampling)
    algo.setBlockSize(blockSize)
    algo.setMaximumCoefficientOfVariation(coefficientOfVariation)
    algo.setMaximumTimeDuration(maximumDurationSeconds)
    initialNumberOfCall = g.getEvaluationCallsNumber()
    algo.run()
    result = algo.getResult()
    numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
    computedProbability = result.getProbabilityEstimate()
    confidenceLength = result.getConfidenceLength(confidenceLevel)
    pmin = computedProbability - 0.5 * confidenceLength
    pmax = computedProbability + 0.5 * confidenceLength
    cov = result.getCoefficientOfVariation()
    if cov > 0.0:
        expectedDigits = -np.log10(cov) - 1.0
    else:
        expectedDigits = 0.0
    stopTime = time.time()
    elapsedTime = stopTime - startTime
    resultArray[i][0] = computedProbability
    resultArray[i][1] = numberOfFunctionEvaluations
    resultArray[i][2] = pmin
    resultArray[i][3] = pmax
    resultArray[i][4] = cov
    resultArray[i][5] = expectedDigits
    resultArray[i][6] = elapsedTime


# %%
df = pd.DataFrame(resultArray, index=model_names, columns=metrics)
# df.to_csv("reliability_compute_reference_proba.csv")
df

# %%
# The problems with higher failture probabilities are obviously solved with more accuracy with the Monte-Carlo method.
# For example, the RP55 problem which has the highest probability equal to 0.560 has more than 3 significant digits.
# On the opposite side, the problems with probabilities close to zero are much more difficult to solve.
# The RP28 with a probability close to :math:`10^{-7}` has no significant digit.
#
# These previous results are consistent with the distribution of the Monte-Carlo estimator.
# The properties of the binomial distribution imply that its variance is:
#
# .. math::
#     \sigma_{p_f}^2 = \frac{p_f (1-p_f)}{n}
#
# where :math:`n` is the sample size and :math:`p_f` is the failure probability.
# The coefficient of variation is:
#
# .. math::
#     CV = \frac{\sigma_{p_f}}{p_f}.
#
# Since we do not know the exact value of :math:`p_f`, we use is approximation :math:`\tilde{p_f}` instead
# (this turns rigorous equations into approximate ones, but does not change the outcome).
# This implies:
#
# .. math::
#     CV = \sqrt{\frac{1 - p_f}{p_f n}}.
#
# When :math:`p_f\rightarrow 0`, we have :math:`p_f \rightarrow 0` which implies:
#
# .. math::
#      CV \rightarrow \sqrt{\frac{1}{p_f n}}.
#
# Inverting the previous equation, we get the sample size given the coefficient of variation:
#
# .. math::
#     n \approx \frac{1}{p_f CV^2}.
#
# This leads to the rule of thumb that, in order to estimate the probability :math:`p_f = 10^{-m}`,
# where :math:`m` is an integer, we need a sample size equal to:
#
# .. math::
#     n \approx \frac{1}{10^{-m} 10^{-2}} = 10^{m+2}.
#
# For example, estimating the probability of the RP28 problem with just one single digit leads to
# a sample size equal to :math:`n=10^9`, since the exact :math:`p_f \approx 10^{-7}`.
