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
        pf_exacte = 0.560
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.0e-4)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0, 0.0]
        Y = function(X)
        assert type(Y) is ot.Point
        np.testing.assert_allclose(Y[0], 0.2)

    def test_UseCaseMonteCarlo(self):
        problem = otb.ReliabilityProblem55()
        event = problem.getEvent()

        # Create a Monte Carlo algorithm
        experiment = ot.MonteCarloExperiment()
        algo = ot.ProbabilitySimulationAlgorithm(event, experiment)
        algo.setMaximumCoefficientOfVariation(0.01)
        algo.setBlockSize(int(1.0e3))
        algo.setMaximumOuterSampling(int(1e3))
        algo.run()
        # Retrieve results
        result = algo.getResult()
        computed_pf = result.getProbabilityEstimate()
        exact_pf = problem.getProbability()
        print("exact_pf=", exact_pf)
        print("computed_pf=", computed_pf)
        samplesize = result.getOuterSampling() * result.getBlockSize()
        alpha = 0.05
        pflen = result.getConfidenceLength(1 - alpha)
        print(
            "%.2f%% confidence interval = [%f,%f]"
            % ((1 - alpha) * 100, computed_pf - pflen / 2, computed_pf + pflen / 2)
        )
        print("Sample size : ", samplesize)
        atol = 1.0e2 / np.sqrt(samplesize)
        np.testing.assert_allclose(computed_pf, exact_pf, atol=atol)


if __name__ == "__main__":
    unittest.main()
