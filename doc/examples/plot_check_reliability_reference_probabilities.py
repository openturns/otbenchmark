"""
Check reliability problems reference probabilities
==================================================
"""

# %%
# In this example, we check that the reference probabilities in the reliability problems
# are consistent with confidence bounds from Monte-Carlo simulations.
# These 95% confidence bounds are stored in 'reliability_compute_reference_proba.csv'
# and required approximately than :math:`10^9` function evaluations for each problem.
#
# We consider two different metrics:
#
# * we check if the reference probability is within the 95% confidence bounds,
# * we compute the number of significant digits by comparing the Monte-Carlo estimator and the reference value.
#
# The number of significant digits may be as high as 17 when all decimal digits are correct.
# However, the reference probabilities are only known up to 3 digits for most problems.
# In order to keep some safeguard, we will be happy with 2 correct digits.
#
# These metrics may fail.
#
# * On average, a fraction equal to 5% of the estimates are outside the confidence bounds.
# * The Monte-Carlo estimator may not be accurate enough, e.g. if the probability is very close to zero.

# %%
import otbenchmark as otb
import pandas as pd


# %%
df = pd.read_csv("reliability_compute_reference_proba.csv")
df


# %%
data = df.values


# %%
pf_reference = data[:, 1]
pmin = data[:, 3]
pmax = data[:, 4]


# %%
benchmarkProblemList = otb.ReliabilityBenchmarkProblemList()
numberOfProblems = len(benchmarkProblemList)
numberOfProblems


# %%
digitsMinimum = 2


# %%
categoryA = []
categoryB = []
categoryC = []
categoryD = []


# %%
for i in range(numberOfProblems):
    problem = benchmarkProblemList[i]
    name = problem.getName()
    pf = problem.getProbability()
    event = problem.getEvent()
    antecedent = event.getAntecedent()
    distribution = antecedent.getDistribution()
    dimension = distribution.getDimension()
    if pf > pmin[i] and pf < pmax[i]:
        tagBounds = "In"
    else:
        tagBounds = "Out"
    digits = otb.ComputeLogRelativeError(pf_reference[i], pf)
    if tagBounds == "In" and digits >= digitsMinimum:
        categoryA.append(name)
    elif tagBounds == "Out" and digits >= digitsMinimum:
        categoryB.append(name)
    elif tagBounds == "In" and digits < digitsMinimum:
        categoryC.append(name)
    else:
        categoryD.append(name)
    print(
        "#%d, %-10s, pf=%.2e, ref=%.2e, C.I.=[%.2e,%.2e], digits=%d : %s"
        % (i, name[0:10], pf, pf_reference[i], pmin[i], pmax[i], digits, tagBounds)
    )

# %%
# There are four different cases.
#
# * Category A: all good. For some problems, both metrics are correct in the sense
#   that the reference probability is within the bounds and the number of significant digits is larger than 2.
#   The RP24, RP55, RP110, RP63, R-S, Axial stressed beam problems fall in that category.
# * Category B: correct digits, not in bounds.
#   We see that the RP8 problem has a reference probability outside of the 95% confidence bounds,
#   but has 2 significant digits.
# * Category C: insufficient digits, in bounds. The difficult RP28 problem fall in that category.
# * Category D: insufficient digits, not in bounds. These are suspicious problems.

# %%
print(categoryA)

# %%
print(categoryB)

# %%
print(categoryC)

# %%
print(categoryD)

# %%
# The number of suspicious problems seems very large.
# However, we notice that all these cases are so that the reference probability is close,
# in absolute value, to the Monte-Carlo estimator.
