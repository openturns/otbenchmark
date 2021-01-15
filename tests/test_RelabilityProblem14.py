# -*- coding: utf-8 -*-
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
        pf_exacte = 0.00752
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.0e-15)

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

    def test_UseCaseFORM(self):
        problem = otb.ReliabilityProblem14()
        event = problem.getEvent()
        distribution = event.getAntecedent().getDistribution()
        # We create a NearestPoint algorithm
        myCobyla = ot.Cobyla()
        # Resolution options:
        eps = 1e-3
        myCobyla.setMaximumEvaluationNumber(1000)
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
        myImportance.setMean(standardSpaceDesignPoint)
        experiment = ot.ImportanceSamplingExperiment(myImportance)
        standardEvent = ot.StandardEvent(event)
        algo = ot.ProbabilitySimulationAlgorithm(standardEvent, experiment)
        algo.setMaximumCoefficientOfVariation(0.01)
        algo.setBlockSize(1000)
        algo.setMaximumOuterSampling(1000)
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
        atol = 1.0e1 / np.sqrt(samplesize)
        np.testing.assert_allclose(computed_pf, exact_pf, atol=atol)


if __name__ == "__main__":
    unittest.main()
