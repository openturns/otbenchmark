"""
Test for FORMFactory class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckFORM(unittest.TestCase):
    def test_FORM(self):
        problem = otb.ReliabilityProblem14()
        nearestPointAlgorithm = ot.AbdoRackwitz()
        algo = otb.FORM(problem, nearestPointAlgorithm)
        algo.run()
        result = algo.getResult()
        pf = result.getEventProbability()
        exactPf = problem.getProbability()
        np.testing.assert_almost_equal(pf, exactPf, decimal=2)


if __name__ == "__main__":
    unittest.main()
