#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute reference Flooding Sobol' indices.
"""

import openturns as ot
import otbenchmark as otb

print("Get Flooding S.A. problem")
problem = otb.FloodingSensitivity()
print(problem)
distribution = problem.getInputDistribution()
model = problem.getFunction()
dimension = distribution.getDimension()

# Create X/Y data
print("Generate training sample")
sample_size_train = 1000
sequence = ot.SobolSequence(distribution.getDimension())
experiment = ot.LowDiscrepancyExperiment(sequence, distribution, sample_size_train)
inputTrain = experiment.generate()
outputTrain = model(inputTrain)

# Create sparse chaos
print("Create sparse chaos")
distributionList = [distribution.getMarginal(i) for i in range(dimension)]
multivariateBasis = ot.OrthogonalProductPolynomialFactory(distributionList)
approximationAlgorithm = ot.LeastSquaresMetaModelSelectionFactory()
projectionStrategy = ot.LeastSquaresStrategy(
    inputTrain, outputTrain, approximationAlgorithm
)
totalDegree = 8

polyColl = [
    ot.StandardDistributionPolynomialFactory(distributionList[i])
    for i in range(dimension)
]
q = 0.5  # the q-quasi-norm parameter
enumerateFunction = ot.HyperbolicAnisotropicEnumerateFunction(dimension, q)
multivariateBasis = ot.OrthogonalProductPolynomialFactory(polyColl, enumerateFunction)

enumfunc = multivariateBasis.getEnumerateFunction()
P = enumfunc.getStrataCumulatedCardinal(totalDegree)
adaptiveStrategy = ot.FixedStrategy(multivariateBasis, P)
chaosalgo = ot.FunctionalChaosAlgorithm(
    inputTrain, outputTrain, distribution, adaptiveStrategy, projectionStrategy
)
print("Fit")
chaosalgo.run()
chaosResult = chaosalgo.getResult()

# Validation
print("Validation")
metamodel = chaosResult.getMetaModel()  # get the metamodel
sample_size_test = 1000
experiment = ot.LowDiscrepancyExperiment(sequence, distribution, sample_size_test)
inputTest = experiment.generate()
outputTest = model(inputTest)
val = ot.MetaModelValidation(inputTest, outputTest, metamodel)
Q2 = val.computePredictivityFactor()[0]
print("Q2=%.2f%%" % (100 * Q2))

# S.A.
print("S.A.")
chaosSI = ot.FunctionalChaosSobolIndices(chaosResult)
first_order_indices = ot.Point([chaosSI.getSobolIndex(i) for i in range(dimension)])
total_order_indices = ot.Point(
    [chaosSI.getSobolTotalIndex(i) for i in range(dimension)]
)


def get_string(point, string_format="%.2f"):
    point_string = [string_format % (point[i]) for i in range(point.getDimension())]
    joined = ",".join(point_string)
    full_string = "[" + joined + "]"
    return full_string


first_order_string = get_string(first_order_indices)
print("First order indices")
print(first_order_string)
total_order_string = get_string(total_order_indices)
print("Total order indices")
print(total_order_string)
