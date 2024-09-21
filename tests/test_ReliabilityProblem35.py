"""
Created on Mon Apr 20 12:42:16 2020

@author: Jebroun
Test for ReliabilityBenchmarkProblem35 class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckReliabilityProblem35(unittest.TestCase):
    def test_ReliabilityBenchmarkProblem35(self):
        problem = otb.ReliabilityProblem35()
        print(problem)

        # Check probability
        pf = problem.getProbability()

        ot.ResourceMap.SetAsScalar("IteratedQuadrature-MaximumError", 1.0e-8)
        ot.ResourceMap.SetAsUnsignedInteger(
            "IteratedQuadrature-MaximumSubIntervals", 256
        )

        # P = P(min(2-x2+exp(-0.1*x1^2)+(0.2*x1)^4,4.5-x1*x2)<0)
        # It can be rewritten as:
        # P = P(A or B) = 1 - P(Ac and Bc)
        # where A = 2-x2+exp(-0.1*x1^2)+(0.2*x1)^4<0, B = 4.5-x1*x2<0
        #       Ac= 2-x2+exp(-0.1*x1^2)+(0.2*x1)^4>0, Bc= 4.5-x1*x2>0
        # So it reduces to compute P'=P(Ac and Bc):
        # P'=\int_{-\infty}^0\int_{4.5/x1}^{2+exp(-0.1*x1^2)+(0.2*x1)^4}phi(x1)phi(x2)dx1dx2+
        #    \int_0^{x1_0}\int_{-\infty}^{2+exp(-0.1*x1^2)+(0.2*x1)^4}phi(x1)phi(x2)dx1dx2
        # +
        #    \int_{x1_0}^{+\infty}\int_{-\infty}^{4.5/x1}phi(x1)phi(x2)dx1dx2
        # where x1_0 solves 2+exp(-0.1*x1^2)+(0.2*x1)^4=4.5/x1
        # i.e. x1_0~1.61838417653828982908750781436
        # Maple gives P=0.00347894632
        lower = ot.SymbolicFunction("x1", "4.5/x1")
        upper = ot.SymbolicFunction("x1", "2+exp(-0.1*x1^2)+(0.2*x1)^4")
        x1_0 = 1.61838417653828982908750781436

        def kernel(X):
            return [ot.Normal(2).computePDF(X)]

        p_part1 = ot.IteratedQuadrature().integrate(
            ot.PythonFunction(2, 1, kernel), -8.5, 0.0, [lower], [upper]
        )[0]
        p_part2 = ot.IteratedQuadrature().integrate(
            ot.PythonFunction(2, 1, kernel),
            0.0,
            x1_0,
            [ot.SymbolicFunction("x1", "-8.5")],
            [upper],
        )[0]
        p_part3 = ot.IteratedQuadrature().integrate(
            ot.PythonFunction(2, 1, kernel),
            x1_0,
            8.5,
            [ot.SymbolicFunction("x1", "-8.5")],
            [lower],
        )[0]
        Pp = p_part1 + p_part2 + p_part3
        pf_exacte = 1 - Pp
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.0e-8)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0, 0.0]
        Y = function(X)
        assert type(Y) is ot.Point
        np.testing.assert_allclose(Y[0], 3)

    def test_UseCase(self):
        problem = otb.ReliabilityProblem35()
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
