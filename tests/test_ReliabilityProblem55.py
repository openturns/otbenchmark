# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 10:22:52 2020

@author: Jebroun

Test for ReliabilityBenchmarkProblem55 class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckReliabilityProblem55(unittest.TestCase):

    def test_ReliabilityBenchmarkProblem55(self):
        problem = otb.ReliabilityProblem55()
        print(problem)

        # Check probability
        pf = problem.getProbability()
        pf_exacte = 0.36
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.e-7)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0, 0.0]
        Y = function(X)
        assert(type(Y) is ot.Point)
        np.testing.assert_allclose(Y[0], 0.2)



if __name__ == "__main__":
    unittest.main()

