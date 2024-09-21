"""
Created on Tue Apr 21 11:22:57 2020

@author: Jebroun

Test for ReliabilityBenchmarkProblem75 class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckReliabilityProblem75(unittest.TestCase):
    def test_ReliabilityBenchmarkProblem75(self):
        problem = otb.ReliabilityProblem75()
        print(problem)

        # Check probability
        pf = problem.getProbability()

        # P = P(3-x1*x2<0)
        # It can be rewritten (taking symmetry into account) as:
        # P = 2\int_0^{\infty}\int_{3/x1}^{\infty}\phi(x1)\phi(x2)dx2dx1
        # Maple gives P=0.981929872154689055665574917800e-2
        # This time we get something meaningfull using distribution's arithmetic
        P = (ot.Normal() * ot.Normal()).computeComplementaryCDF(3.0)
        print("(Distribution arithmetic) P=", P)
        lower = ot.SymbolicFunction("x1", "3/x1")
        upper = ot.SymbolicFunction("x1", "8.5")

        def kernel(X):
            return [ot.Normal(2).computePDF(X)]

        half_p = ot.IteratedQuadrature().integrate(
            ot.PythonFunction(2, 1, kernel), 0, 8.5, [lower], [upper]
        )[0]
        pf_exacte = 2 * half_p
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.0e-9)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0, 0.0]
        Y = function(X)
        assert type(Y) is ot.Point
        np.testing.assert_allclose(Y[0], 3)

    def test_UseCase(self):
        problem = otb.ReliabilityProblem75()
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
