# -*- coding: utf-8 -*-
"""
Test for SORMFactory class.
"""
import otbenchmark as otb
import unittest
import numpy as np


class CheckSORMFactory(unittest.TestCase):
    def test_SORMFactory(self):
        problem = otb.ReliabilityProblem14()
        algo = otb.SORMFactory(problem)
        algo.run()
        result = algo.getResult()
        pf = result.getEventProbabilityBreitung()
        exactPf = problem.getProbability()
        np.testing.assert_almost_equal(pf, exactPf, decimal=2)


if __name__ == "__main__":
    unittest.main()
