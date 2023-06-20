# -*- coding: utf-8 -*-
"""
Test for RequestedBBRCProblem class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckRequestedBBRCProblem(unittest.TestCase):
    def test_RequestedBBRCProblem(self):
        problem = otb.RequestedBBRCProblem("testuser", "testpass", -1, 1)
        print(problem)

        # Check probability
        pf = problem.getProbability()
        pf_exacte = 0.0007888456943755395
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.0e-15)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0] * 6
        Y = function(X)
        assert type(Y) is ot.Point
        np.testing.assert_allclose(Y[0], 0)


if __name__ == "__main__":
    unittest.main()
