# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 14:39:26 2020

@author: Jebroun

Class to define the ReliabilityProblem107 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem107(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, mu=0, sigma=1):
        """
        Creates a reliability problem RP107.

        The event is {g(X) < threshold} where

        X = (x1, x2, ...., x10)

        g(X) = 5*sqrt(10) -(x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10).

        We have xi ~ Normal(0, 1) for i in {1, 2, ...,10}

        Parameters
        ----------
        threshold : float
            The threshold.
        mu : float
            The mean of the Xi Normal distribution for i in {1, 2, ..., 10}.
        sigma : float
            The standard deviation of the Xi Normal distribution
            for i in {1, 2, ..., 10}.
        """

        formula = "5*sqrt(10)-(x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10)"

        limitStateFunction = ot.SymbolicFunction(
            ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10"], [formula]
        )

        X = [ot.Normal(mu, sigma) for i in range(10)]

        myDistribution = ot.ComposedDistribution(X)
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP107"
        probability = 0.000000292
        super(ReliabilityProblem107, self).__init__(name, thresholdEvent, probability)
        return None
