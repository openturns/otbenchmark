"""
Test for SORMFactory class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckSORM(unittest.TestCase):
    def test_SORM(self):
        problem = otb.ReliabilityProblem14()
        nearestPointAlgorithm = ot.AbdoRackwitz()
        algo = otb.SORM(problem, nearestPointAlgorithm)
        algo.run()
        result = algo.getResult()
        pf = result.getEventProbabilityBreitung()
        exactPf = problem.getProbability()
        np.testing.assert_almost_equal(pf, exactPf, decimal=2)


if __name__ == "__main__":
    unittest.main()
