# -*- coding: utf-8 -*-
"""
Test for FORMISFactory class.
"""
import otbenchmark as otb
import unittest
import numpy as np


class CheckFORMISFactory(unittest.TestCase):
    def test_FORMISFactory(self):
        problem = otb.ReliabilityProblem14()
        algo = otb.FORMISFactory(problem)
        algo.run()
        result = algo.getResult()
        pf = result.getProbabilityEstimate()
        exactPf = problem.getProbability()
        np.testing.assert_almost_equal(pf, exactPf, decimal=2)


if __name__ == "__main__":
    unittest.main()
