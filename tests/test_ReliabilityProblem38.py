# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 12:45:56 2020

@author: Jebroun


Test for ReliabilityBenchmarkProblem38 class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckReliabilityProblem38(unittest.TestCase):
    def test_ReliabilityBenchmarkProblem38(self):
        problem = otb.ReliabilityProblem38()
        print(problem)

        # Check probability
        pf = problem.getProbability()
        pf_exacte = 0.0081
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.0e-15)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0]
        Y = function(X)
        assert type(Y) is ot.Point
        np.testing.assert_allclose(Y[0], 15.59 * 1e4)

    def test_UseCase(self):
        problem = otb.ReliabilityProblem38()
        event = problem.getEvent()

        # Create a Monte Carlo algorithm
        experiment = ot.MonteCarloExperiment()
        algo = ot.ProbabilitySimulationAlgorithm(event, experiment)
        algo.setMaximumCoefficientOfVariation(0.05)
        algo.setMaximumOuterSampling(int(1e5))
        algo.run()

        # Retrieve results
        result = algo.getResult()
        computed_pf = result.getProbabilityEstimate()
        exact_pf = problem.getProbability()
        print("exact_pf=", exact_pf)
        print("computed_pf=", computed_pf)
        samplesize = result.getOuterSampling() * result.getBlockSize()
        print("Sample size : ", samplesize)
        atol = 1.0 / np.sqrt(samplesize)
        np.testing.assert_allclose(computed_pf, exact_pf, atol=atol)


if __name__ == "__main__":
    unittest.main()
