"""
Print a reliability benchmark problem
=====================================
"""

# %%
import otbenchmark as otb

# %%
problem = otb.RminusSReliability()
print(problem)

# %%
print(problem.toFullString())

# %%
problem.getName()

# %%
event = problem.getEvent()

# %%
g = event.getFunction()
g

# %%
event.getOperator()

# %%
threshold = event.getThreshold()
threshold

# %%
pf = problem.getProbability()
pf

# %%
beta = problem.computeBeta()
beta

# %%
inputVector = event.getAntecedent()
distribution = inputVector.getDistribution()
distribution
