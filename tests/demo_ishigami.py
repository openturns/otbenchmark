# -*- coding: utf-8 -*-
"""A demo of the IshigamiSensitivityBenchmarkProblem class."""

import otbenchmark as otb
import openturns as ot

problem = otb.IshigamiSensitivityBenchmarkProblem()
distribution = problem.getInputDistribution()
model = problem.getFunction()

# Create X/Y data
ot.RandomGenerator.SetSeed(0)
size = 1000
inputDesign = ot.SobolIndicesExperiment(distribution, size, True).generate()
outputDesign = model(inputDesign)

# Compute first order indices using the Saltelli estimator
sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(inputDesign, outputDesign, size)
computed_first_order = sensitivityAnalysis.getFirstOrderIndices()

# Compare with exact results
exact_first_order = problem.getFirstOrderIndices()
print("Exact S=", exact_first_order)
dimension = distribution.getDimension()
# Compute absolute error (the LRE cannot be computed, because S can be zero)
for i in range(dimension):
    absoluteError = abs(computed_first_order[i] - exact_first_order[i])
    print("Indice #", i, ", Abs.Err.=", absoluteError)
