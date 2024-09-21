# Copyright 2020 EDF
"""
Test for FourBranchSerialSystemReliability class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckFourBranchSerialSystemReliability(unittest.TestCase):
    def test_FourBranchSerialSystemReliability(self):
        problem = otb.FourBranchSerialSystemReliability()
        print(problem)

        # Check probability
        pf = problem.getProbability()

        # The innermost integral has a closed-form:
        # P = 1-4\int_{0}^{7/2}(Phi(3+0.2*u^2)-1/2)\phi(u)du
        def f(x):
            u = x[0]
            pnormal = ot.DistFunc.pNormal(3 + 0.2 * u ** 2) - 0.5
            return [pnormal * np.exp(-(u ** 2) / 2) * ot.SpecFunc.ISQRT2PI]

        part_of_p = ot.GaussKronrod().integrate(
            ot.PythonFunction(1, 1, f), ot.Interval(0, 7 / 2)
        )[0]

        pf_exacte = 1 - 4 * part_of_p
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.0e-12)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [1.0, -1.0]
        Y = function(X)
        assert type(Y) is ot.Point
        np.testing.assert_allclose(Y[0], 2.9497474683058327)

    def test_UseCase(self):
        problem = otb.RminusSReliability()
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
