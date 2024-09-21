# Copyright 2020 EDF.
"""
Test for ConditionalDistribution class.
"""
import otbenchmark
import unittest


class CheckCrossCutFunction(unittest.TestCase):
    def test_CrossCutFunction(self):
        problem = otbenchmark.ReliabilityProblem33()
        event = problem.getEvent()
        g = event.getFunction()
        inputVector = event.getAntecedent()
        distribution = inputVector.getDistribution()

        alpha = 1 - 0.00001
        (
            bounds,
            marginalProb,
        ) = distribution.computeMinimumVolumeIntervalWithMarginalProbability(alpha)

        referencePoint = distribution.getMean()
        crossCut = otbenchmark.CrossCutFunction(g, referencePoint)
        try:
            _ = crossCut.draw(bounds)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    unittest.main()
