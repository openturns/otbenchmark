# -*- coding: utf-8 -*-
"""A demo of the AxialStressedBeamReliabilityBenchmarkProblem class."""

import otbenchmark as otb
import openturns as ot
import numpy as np

problem = otb.AxialStressedBeamReliabilityBenchmarkProblem()
event = problem.getEvent()

# Create a Monte Carlo algorithm
experiment = ot.MonteCarloExperiment()
algo = ot.ProbabilitySimulationAlgorithm(event, experiment)
algo.setMaximumCoefficientOfVariation(0.05)
algo.setMaximumOuterSampling(int(1e5))
algo.run()

# Retrieve results
result = algo.getResult()
computed_pf = result.getProbabilityEstimate()
print("Computed Pf=", computed_pf)

# Compare with exact results
exact_pf = problem.getProbability()
print("Exact Pf=", exact_pf)
# Compute log-relative error
log_relative_error = -np.log10(abs(computed_pf - exact_pf) / exact_pf)
print("Number of correct digits=", log_relative_error)
