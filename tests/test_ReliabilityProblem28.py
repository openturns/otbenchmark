"""
Created on Mon Apr 20 10:55:16 2020

@author: Jebroun

Test for ReliabilityBenchmarkProblem28 class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckReliabilityProblem28(unittest.TestCase):
    def test_ReliabilityBenchmarkProblem28(self):
        problem = otb.ReliabilityProblem28()
        print(problem)

        # Check probability
        pf = problem.getProbability()
        pf_exacte = 0.000000146
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.0e-2)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0, 0.0]
        Y = function(X)
        assert type(Y) is ot.Point
        np.testing.assert_allclose(Y[0], 0.0)

    def test_UseCase(self):
        problem = otb.ReliabilityProblem28()
        event = problem.getEvent()

        # Create a Monte Carlo algorithm
        experiment = ot.MonteCarloExperiment()
        algo = ot.ProbabilitySimulationAlgorithm(event, experiment)
        algo.setMaximumCoefficientOfVariation(0.01)
        algo.setBlockSize(512)
        algo.setMaximumOuterSampling(1000)
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
        print("atol=", atol)
        np.testing.assert_allclose(computed_pf, exact_pf, atol=atol)

    def test_UseCaseFORMIS(self):
        problem = otb.ReliabilityProblem28()

        factory = otb.ProbabilitySimulationAlgorithmFactory()
        nearestPointAlgorithm = ot.AbdoRackwitz()
        algo = factory.buildFORMIS(problem, nearestPointAlgorithm)
        algo.setMaximumCoefficientOfVariation(0.01)
        algo.setMaximumOuterSampling(1000)
        algo.setBlockSize(512)
        algo.run()
        result = algo.getResult()
        computed_pf = result.getProbabilityEstimate()
        print("computed_pf=", computed_pf)
        exact_pf = problem.getProbability()
        print("exact_pf=", exact_pf)
        samplesize = result.getOuterSampling() * result.getBlockSize()
        print("Sample size : ", samplesize)
        atol = 1.0 / np.sqrt(samplesize)
        print("atol=", atol)
        np.testing.assert_allclose(computed_pf, exact_pf, atol=atol)
        alpha = 0.05
        pflen = result.getConfidenceLength(1.0 - alpha)
        pf_low = computed_pf - pflen / 2.0
        pf_up = computed_pf + pflen / 2.0
        print(
            "%.2f%% confidence interval = [%f,%f] * 1.e-7"
            % ((1.0 - alpha) * 100, 1.0e7 * pf_low, 1.0e7 * pf_up)
        )


if __name__ == "__main__":
    unittest.main()
