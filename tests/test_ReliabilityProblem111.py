# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:05:02 2020

@author: Jebroun
Test for ReliabilityBenchmarkProblem111 class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckReliabilityProblem111(unittest.TestCase):

    def test_ReliabilityBenchmarkProblem111(self):
        problem = otb.ReliabilityProblem111()
        print(problem)

        # Check probability
        pf = problem.getProbability()
        pf_exacte = 7.65e-7
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.e-15)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0, 0.0]
        Y = function(X)
        assert(type(Y) is ot.Point)
        np.testing.assert_allclose(Y[0], 12.5)

    def test_UseCase(self):
        problem = otb.ReliabilityProblem111()
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
        print('exact_pf=', exact_pf)
        print('computed_pf=', computed_pf)
        samplesize = result.getOuterSampling() * result.getBlockSize()
        print("Sample size : ", samplesize)
        atol = 1.0 / np.sqrt(samplesize)
        np.testing.assert_allclose(computed_pf, exact_pf, atol=atol)

if __name__ == "__main__":
    unittest.main()

