"""
Test for ProbabilitySimulationAlgorithmFactory class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckProbabilitySimulationAlgorithmFactory(unittest.TestCase):
    def test_MonteCarlo(self):
        problem = otb.ReliabilityProblem14()
        factory = otb.ProbabilitySimulationAlgorithmFactory()
        algo = factory.buildMonteCarlo(problem)
        algo.setMaximumOuterSampling(100000)
        algo.run()
        result = algo.getResult()
        pf = result.getProbabilityEstimate()
        exactPf = problem.getProbability()
        np.testing.assert_almost_equal(pf, exactPf, decimal=2)

    def test_FORMIS(self):
        problem = otb.ReliabilityProblem14()
        nearestPointAlgorithm = ot.AbdoRackwitz()
        factory = otb.ProbabilitySimulationAlgorithmFactory()
        algo = factory.buildFORMIS(problem, nearestPointAlgorithm)
        algo.run()
        result = algo.getResult()
        pf = result.getProbabilityEstimate()
        exactPf = problem.getProbability()
        np.testing.assert_almost_equal(pf, exactPf, decimal=2)


if __name__ == "__main__":
    unittest.main()
