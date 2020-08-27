# -*- coding: utf-8 -*-
"""
Test for MonteCarloFactory class.
"""
import otbenchmark as otb
import unittest
import numpy as np


class CheckMonteCarloFactory(unittest.TestCase):
    def test_MCFactory(self):
        problem = otb.ReliabilityProblem14()
        algo = otb.MonteCarloFactory(problem)
        algo.setMaximumOuterSampling(100000)
        algo.run()
        result = algo.getResult()
        pf = result.getProbabilityEstimate()
        exactPf = problem.getProbability()
        np.testing.assert_almost_equal(pf, exactPf, decimal=2)


if __name__ == "__main__":
    unittest.main()
