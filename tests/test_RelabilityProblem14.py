"""
Created on Wed Apr 29 11:50:49 2020

@author: Jebroun

Test for ReliabilityBenchmarkProblem14 class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckReliabilityProblem14(unittest.TestCase):
    def test_ReliabilityBenchmarkProblem14(self):
        problem = otb.ReliabilityProblem14()
        print(problem)

        # Check probability
        pf = problem.getProbability()

        a = 70.0
        b = 80.0
        mu2 = 39.0
        sigma2 = 0.1
        mu3 = 1500.0
        sigma3 = 350.0
        mu4 = 400.0
        sigma4 = 0.1
        mu5 = 250000.0
        sigma5 = 35000.0
        X1 = ot.Uniform(a, b)
        X1.setDescription(["X1"])
        X2 = ot.Normal(mu2, sigma2)
        X2.setDescription(["X2"])
        param3 = ot.GumbelMuSigma(mu3, sigma3)
        X3 = ot.ParametrizedDistribution(param3)
        X3.setDescription(["X3"])
        X4 = ot.Normal(mu4, sigma4)
        X4.setDescription(["X4"])
        X5 = ot.Normal(mu5, sigma5)
        X5.setDescription(["X5"])
        # Here we can use IteratedQuadrature with different underlying 1D algorithms
        # We use a SymbolicFunction, much more efficient than a PythonFunction
        Xreduced = ot.ComposedDistribution([X2, X3, X4, X5])

        bet, gam = param3.getDistribution().getParameter()
        formula = "max(0, min(1, 32/(pi_*x2^3)*sqrt(x3^2*x4^2/16+x5^2)/10 - 7))*"
        formula += "exp(-0.5*((x2-39)^2/0.1^2+(x4-400)^2/0.1^2+(x5-250000)^2/35000^2))/"
        formula += "((2*pi_)^(3/2)*0.1*0.1*35000)*exp(-(x3-"
        formula += str(gam) + ") / " + str(bet) + "-exp(-(x3-" + str(gam)
        formula += ") / " + str(bet) + ")) / " + str(bet)

        fun = ot.SymbolicFunction(["x2", "x3", "x4", "x5"], [formula])

        # The full loop takes a llllooonnnggg time to complete!
        N = 5
        pf_exacte = ot.IteratedQuadrature(ot.GaussLegendre([2 ** N])).integrate(
            fun, Xreduced.getRange()
        )[0]

        np.testing.assert_allclose(pf, pf_exacte, rtol=1.0e-1)

        # Check function
        event = problem.getEvent()
        function = event.getFunction()
        X = [0.0, 1.0, 0.0, 0.0, 0.0]
        Y = function(X)
        assert type(Y) is ot.Point
        np.testing.assert_allclose(Y[0], 0.0)

    def test_UseCaseMonteCarlo(self):
        problem = otb.ReliabilityProblem14()
        event = problem.getEvent()

        # Create a Monte Carlo algorithm
        experiment = ot.MonteCarloExperiment()
        algo = ot.ProbabilitySimulationAlgorithm(event, experiment)
        algo.setMaximumCoefficientOfVariation(0.01)
        algo.setBlockSize(int(1.0e2))
        algo.setMaximumOuterSampling(int(1e2))
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
        atol = 1.0 / np.sqrt(samplesize)
        np.testing.assert_allclose(computed_pf, exact_pf, atol=atol)

    def test_UseCaseFORM(self):
        problem = otb.ReliabilityProblem14()
        event = problem.getEvent()
        distribution = event.getAntecedent().getDistribution()
        # We create a NearestPoint algorithm
        myCobyla = ot.Cobyla()
        # Resolution options:
        eps = 1e-2
        myCobyla.setMaximumCallsNumber(1000)
        myCobyla.setMaximumAbsoluteError(eps)
        myCobyla.setMaximumRelativeError(eps)
        myCobyla.setMaximumResidualError(eps)
        myCobyla.setMaximumConstraintError(eps)
        # For statistics about the algorithm
        algo = ot.FORM(myCobyla, event, distribution.getMean())
        algo.run()
        resultFORM = algo.getResult()
        # Combine with Importance Sampling
        standardSpaceDesignPoint = resultFORM.getStandardSpaceDesignPoint()
        dimension = distribution.getDimension()
        myImportance = ot.Normal(dimension)
        myImportance.setMu(standardSpaceDesignPoint)
        experiment = ot.ImportanceSamplingExperiment(myImportance)
        standardEvent = ot.StandardEvent(event)
        algo = ot.ProbabilitySimulationAlgorithm(standardEvent, experiment)
        algo.setMaximumCoefficientOfVariation(0.01)
        algo.setBlockSize(1000)
        algo.setMaximumOuterSampling(100)
        algo.run()
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
        atol = 1.0 / np.sqrt(samplesize)
        np.testing.assert_allclose(computed_pf, exact_pf, atol=atol)


if __name__ == "__main__":
    unittest.main()
