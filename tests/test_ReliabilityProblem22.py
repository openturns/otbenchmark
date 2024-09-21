"""
Created on Mon Apr 20 10:55:16 2020

@author: Jebroun

Test for ReliabilityBenchmarkProblem22 class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckReliabilityProblem22(unittest.TestCase):
    def test_ReliabilityBenchmarkProblem22(self):
        problem = otb.ReliabilityProblem22()
        print(problem)

        # Check probability
        pf = problem.getProbability()

        # The innermost integral has a closed-form:
        # P = \int_{x1_0}^{\infty}Phi(5\sqrt{2}/2+x1+\sqrt{-50+40\sqrt{2}x1}/2)
        #     -Phi(5\sqrt{2}/2+x1-\sqrt{-50+40\sqrt{2}x1}/2)\phi(x1)dx1
        def f(x):
            x1 = x[0]
            pnormal1 = ot.DistFunc.pNormal(
                5 * np.sqrt(2) / 2 + x1 + np.sqrt(-50 + 40 * np.sqrt(2) * x1) / 2
            )
            pnormal2 = ot.DistFunc.pNormal(
                5 * np.sqrt(2) / 2 + x1 - np.sqrt(-50 + 40 * np.sqrt(2) * x1) / 2
            )
            return [
                (pnormal1 - pnormal2) * np.exp(-(x1 ** 2) / 2) * ot.SpecFunc.ISQRT2PI
            ]

        x1_0 = 5 * np.sqrt(2) / 8
        pf_exacte = ot.GaussKronrod().integrate(
            ot.PythonFunction(1, 1, f), ot.Interval(x1_0, 10.0)
        )[0]
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.0e-11)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0, 0.0]
        Y = function(X)
        assert type(Y) is ot.Point
        np.testing.assert_allclose(Y[0], 2.5)

    def test_UseCase(self):
        problem = otb.ReliabilityProblem22()
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
        alpha = 0.05
        pflen = result.getConfidenceLength(1 - alpha)
        print(
            "%.2f%% confidence interval = [%f,%f]"
            % ((1 - alpha) * 100, computed_pf - pflen / 2, computed_pf + pflen / 2)
        )
        atol = 1.0e-1 / np.sqrt(samplesize)
        print("Absolute tolerance: ", atol)
        np.testing.assert_allclose(computed_pf, exact_pf, atol=atol)


if __name__ == "__main__":
    unittest.main()
