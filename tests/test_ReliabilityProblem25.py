"""
Created on Mon Apr 20 10:55:16 2020

@author: Jebroun

Test for ReliabilityBenchmarkProblem25 class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckReliabilityProblem25(unittest.TestCase):
    def test_ReliabilityBenchmarkProblem25(self):
        problem = otb.ReliabilityProblem25()
        print(problem)

        # Check probability
        pf = problem.getProbability()

        # P = P(max(x1^2-8x2+16,-16x1+x2+32)<0)
        # It can be rewritten as:
        # P = \int_{x1_0}^\{x1_1}\int_{2+x1^2/8}^{16x1-32}\phi(x1)\phi(x2)dx2dx1
        # where x1_0 and x1_1 solve 16*x1_0-32=2+x1^2/8 i.e.
        # x1_0=64-4sqrt(239)~2.1615006650387739213966284668
        # x1_1=64-4sqrt(239)~125.838499334961226078603371533
        # Maple gives P=0.41485662937597470791345e-4
        lower = ot.SymbolicFunction("x1", "2+x1^2/8")
        upper = ot.SymbolicFunction("x1", "16*x1-32")
        x1_0 = 64 - 4 * np.sqrt(239)
        x1_1 = 64 + 4 * np.sqrt(239)

        def kernel(X):
            return [ot.Normal(2).computePDF(X)]

        pf_exact = ot.IteratedQuadrature().integrate(
            ot.PythonFunction(2, 1, kernel), x1_0, x1_1, [lower], [upper]
        )[0]

        np.testing.assert_allclose(pf, pf_exact, rtol=1.0e-6)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0, 0.0]
        Y = function(X)
        assert type(Y) is ot.Point
        np.testing.assert_allclose(Y[0], 32.0)

    def test_UseCase(self):
        problem = otb.ReliabilityProblem25()
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
        atol = 1.0e-2 / np.sqrt(samplesize)
        print("Absolute tolerance: ", atol)
        np.testing.assert_allclose(computed_pf, exact_pf, atol=atol)


if __name__ == "__main__":
    unittest.main()
