# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 14:20:07 2020

@author: Jebroun

Class to define the ReliabilityProblem54 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem54(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, expo=1):
        """
        Creates a reliability problem RP54.

        The event is {g(X) < threshold} where

        X = (x1, x2, ..., x20)

        g(X) = (x1 + x2 + ... + x20) - 8.951

        Parameters
        ----------
        threshold : float
            The threshold.
        expo : float
            Rate parameter of the Xi Exponential distribution
            for i in {1, 2, ..., 20}.
        """

        formula = "x1 + x2 + x3 + x4 + x5 + "
        formula += "x6 + x7 + x8 + x9 + x10"
        formula += "+ x11 + x12 + x13 + x14 + x15 +"
        formula += "x16 + x17 + x18 + x19 + x20 - 8.951"

        limitStateFunction = ot.SymbolicFunction(
            [
                "x1",
                "x2",
                "x3",
                "x4",
                "x5",
                "x6",
                "x7",
                "x8",
                "x9",
                "x10",
                "x11",
                "x12",
                "x13",
                "x14",
                "x15",
                "x16",
                "x17",
                "x18",
                "x19",
                "x20",
            ],
            [formula],
        )

        X = [ot.Exponential(expo) for i in range(20)]

        myDistribution = ot.ComposedDistribution(X)
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP54"
        probability = 0.000998
        super(ReliabilityProblem54, self).__init__(name, thresholdEvent, probability)
        return None
