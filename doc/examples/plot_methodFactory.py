"""
Demonstration of the Factory classes for reliability problems
=============================================================
"""

# %%
# In this example, we show how to use various classes which provide an easy way to create an algorithm
# to estimate a problem from a `ReliabilityBenchmarkProblem`.
# This methods do not set the parameters of the algorithm and do not run it,
# so that we can set specific settings for a given problem.

# %%
import openturns as ot
import numpy as np
import otbenchmark as otb

# %%
# We consider the RP8 problem.
problem = otb.ReliabilityProblem8()

# %%
# Create a Monte-Carlo algorithm
# ------------------------------

# %%
# The `buildMonteCarlo` method creates a `ProbabilitySimulationAlgorithm` based on MonteCarlo sampling.
# Before running the algorithm, we set the number of outer iterations based on the `setMaximumOuterSampling` method.
# This shows the main utility of the `Factory` classes.

# %%
factory = otb.ProbabilitySimulationAlgorithmFactory()
algo = factory.buildMonteCarlo(problem)
algo.setMaximumOuterSampling(100000)
algo.run()
result = algo.getResult()
result.getProbabilityEstimate()

# %%
# Create a FORM algorithm
# -----------------------

# %%
# We use the `FORM` class applied to the `problem`.
nearestPointAlgorithm = ot.AbdoRackwitz()
algo = otb.FORM(problem, nearestPointAlgorithm)

# %%
# The `FORM` object of the otbenchmark module implements a `FORM` object from the OpenTURNS library.
# Hence, it has a `run` method. If specific setting is required, we can do it now, prior to the call to the `run` method.
algo.run()

# %%
result = algo.getResult()
result.getEventProbability()


# %%
# We can compare the previous estimate with the exact probability.
problem.getProbability()

# %%
# Create a SORM algorithm
# -----------------------

# %%
# The `SORM` class creates a `SORM` object.
nearestPointAlgorithm = ot.AbdoRackwitz()
algo = otb.SORM(problem, nearestPointAlgorithm)

# %%
algo.run()

# %%
result = algo.getResult()
result.getEventProbabilityBreitung()

# %%
# Create a FORM-IS algorithm
# --------------------------

# %%
# The `buildFORMIS` method of the `ProbabilitySimulationAlgorithmFactory` class creates
# a `ProbabilitySimulationAlgorithm` object, based on the Importance Sampling method
# using the FORM design point with gaussian importance distribution.

# %%
factory = otb.ProbabilitySimulationAlgorithmFactory()
nearestPointAlgorithm = ot.AbdoRackwitz()
algo = factory.buildFORMIS(problem, nearestPointAlgorithm)
algo.run()
result = algo.getResult()
result.getProbabilityEstimate()


# %%
# Create a SubsetSampling algorithm
# ---------------------------------

# %%
algo = otb.SubsetSampling(problem)
algo.run()
result = algo.getResult()
result.getProbabilityEstimate()

# %%
# Create a LHS algorithm
# ----------------------

# %%
algo = otb.LHS(problem)
algo.run()
result = algo.getResult()
result.getProbabilityEstimate()
