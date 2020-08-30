# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 10:22:51 2020

@author: Jebroun
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem55(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, a=[-1.0] * 2, b=[1.0] * 2):
        """
        Creates a reliability problem RP55.

        The event is {g(X) < threshold} where

        X = (x1, x2)

        g1 = 0.2 + 0.6 * (x1 - x2)^4 - (x1 - x2) / sqrt(2)

        g2 = 0.2 + 0.6 * (x1 - x2)^4 + (x1 - x2) / sqrt(2)

        g3 = (x1 - x2) + 5 / sqrt(2) - 2.2

        g4 = (x2 - x1) + 5 / sqrt(2) - 2.2

        g(X) = min(g1, g2, g3, g4)

        We have x1 ~ Uniform(a[0], b[0]) and x2 ~ Uniform(a[1], b[1]).

        Parameters
        ----------
        threshold : float
            The threshold.
        b  : sequence of floats
            The list of two items representing the upper
            bounds of the Uniform distribution.
        a : sequence of floats
            The list of two items representing the lower
            bounds of the Uniform distribution.
        """
        equations = ["var g1 := 0.2 + 0.6 * (x1 - x2)^4 - (x1 - x2) / sqrt(2)"]
        equations.append("var g2 := 0.2 + 0.6 * (x1 - x2)^4 + (x1 - x2) / sqrt(2)")
        equations.append("var g3 := (x1 - x2) + 5 / sqrt(2) - 2.2")
        equations.append("var g4 := (x2 - x1) + 5 / sqrt(2) - 2.2")
        equations.append("gsys := min(g1, g2, g3, g4)")
        formula = ";".join(equations)
        limitStateFunction = ot.SymbolicFunction(["x1", "x2"], ["gsys"], formula)
        inputDimension = len(a)
        if inputDimension != 2:
            raise Exception(
                "The dimension of a is %d, but the expected dimension is 2."
                % (inputDimension)
            )

        inputDimension = len(b)
        if inputDimension != 2:
            raise Exception(
                "The dimension of b is %d, but the expected dimension is 2."
                % (inputDimension)
            )
        X1 = ot.Uniform(a[0], b[0])
        X1.setDescription(["X1"])
        X2 = ot.Uniform(a[1], b[1])
        X2.setDescription(["X2"])

        myDistribution = ot.ComposedDistribution([X1, X2])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP55"
        probability = 5.60014428286370380e-01
        super(ReliabilityProblem55, self).__init__(name, thresholdEvent, probability)
        return None
