"""
Created on Mon Apr 20 12:32:41 2020

@author: Jebroun

Test for ReliabilityBenchmarkProblem31 class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckReliabilityProblem31(unittest.TestCase):
    def test_ReliabilityBenchmarkProblem31(self):
        problem = otb.ReliabilityProblem31()
        print(problem)

        # Check probability
        pf = problem.getProbability()

        # The probability is equal to
        # P=\int_{-\infty}^\infty \int_{2+256*x1^4}^\infty \phi(xi)\phi(x2)dx2dx1
        # Maple gives P=0.322668120958769103770120768386e-2
        lower = ot.SymbolicFunction("x1", "2+256*x1^4")
        upper = ot.SymbolicFunction("x1", "8.5")

        def kernel(X):
            return [ot.Normal(2).computePDF(X)]

        pf_exacte = ot.IteratedQuadrature().integrate(
            ot.PythonFunction(2, 1, kernel), -8.5, 8.5, [lower], [upper]
        )[0]

        np.testing.assert_allclose(pf, pf_exacte, rtol=1.0e-6)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0, 0.0]
        Y = function(X)
        assert type(Y) is ot.Point
        np.testing.assert_allclose(Y[0], 2)

    def test_UseCaseMonteCarlo(self):
        problem = otb.ReliabilityProblem31()
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
        atol = 1.0e-1 / np.sqrt(samplesize)
        print("Absolute tolerance: ", atol)
        np.testing.assert_allclose(computed_pf, exact_pf, atol=atol)


if __name__ == "__main__":
    unittest.main()
