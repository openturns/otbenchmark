# -*- coding: utf-8 -*-
"""
Create a ProbabilitySimulationAlgorithm based on a reliability problem.
"""

import openturns as ot


class ProbabilitySimulationAlgorithmFactory:
    def __init__(self):
        """
        Creates a ProbabilitySimulationAlgorithm algorithm.
        """
        return None

    def buildMonteCarlo(self, problem):
        """
        Creates a Monte-Carlo algorithm.

        We create a MonteCarloExperiment and we create
        a ProbabilitySimulationAlgorithm based on the problem event.

        Parameters
        ----------
        problem : ot.ReliabilityBenchmarkProblem
            The problem.

        Returns
        ----------
        algo : ot.ProbabilitySimulationAlgorithm
            The Monte-Carlo algorithm for estimating the probability.
        """
        myEvent = problem.getEvent()
        experiment = ot.MonteCarloExperiment()
        algo = ot.ProbabilitySimulationAlgorithm(myEvent, experiment)
        return algo

    def buildFORMIS(self, problem, nearestPointAlgorithm):
        """
        Creates a FORM-IS algorithm.

        We first create a FORM object based on the AbdoRackwitz
        and run it to get the design point in the standard space.
        Then we create an ImportanceSamplingExperiment based on the gaussian
        distribution, centered on the design point.
        Finally, we create a ProbabilitySimulationAlgorithm.

        Parameters
        ----------
        problem : ot.ReliabilityBenchmarkProblem
            The problem.
        nearestPointAlgorithm : ot.OptimizationAlgorithm
            Optimization algorithm used to search the design point.

        Returns
        ----------
        algo : ot.ProbabilitySimulationAlgorithm
            The FORM-IS algorithm for estimating the probability.
        """
        event = problem.getEvent()
        inputVector = event.getAntecedent()
        myDistribution = inputVector.getDistribution()
        physicalStartingPoint = myDistribution.getMean()
        algoFORM = ot.FORM(nearestPointAlgorithm, event, physicalStartingPoint)
        algoFORM.run()
        resultFORM = algoFORM.getResult()
        standardSpaceDesignPoint = resultFORM.getStandardSpaceDesignPoint()
        d = myDistribution.getDimension()
        myImportance = ot.Normal(d)
        myImportance.setMean(standardSpaceDesignPoint)
        experiment = ot.ImportanceSamplingExperiment(myImportance)
        standardEvent = ot.StandardEvent(event)
        algo = ot.ProbabilitySimulationAlgorithm(standardEvent, experiment)
        return algo
