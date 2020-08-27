# -*- coding: utf-8 -*-
"""
Test for FORMFactory class.
"""
import otbenchmark as otb
import unittest
import numpy as np


class CheckFORMFactory(unittest.TestCase):
    def test_FORMFactory(self):
        problem = otb.ReliabilityProblem14()
        algo = otb.FORMFactory(problem)
        algo.run()
        result = algo.getResult()
        pf = result.getEventProbability()
        exactPf = problem.getProbability()
        np.testing.assert_almost_equal(pf, exactPf, decimal=2)


if __name__ == "__main__":
    unittest.main()
