# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 10:52:22 2020

@author: Jebroun
Class to define the ReliabilityProblem57 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem57(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, mu=[0.0] * 2, sigma=[1.0] * 2):
        """
        Creates a reliability problem RP57.

        The event is {g(X) < threshold} where

        g(x1, x2) = min(max(g1, g2), g3) with

        g1 = -x1^2 + x2^3 + 3

        g2 = 2 - x1 - 8 * x2

        g3 = (x1 + 3)^2 + (x2 + 3)^2 - 4

        We have x1 ~ Normal(mu[0], sigma[0]) and x2 ~ Normal(mu[1], sigma[1]).

        Parameters
        ----------
        threshold : float
            The threshold.
        mu : sequence of floats
            The list of two items representing the means of the gaussian distributions.
        sigma : float
            The list of two items representing the standard deviations of
            the gaussian distributions.
        """
        equations = ["var g1 := -x1^2 + x2^3 + 3"]
        equations.append("var g2 := 2 - x1 - 8 * x2")
        equations.append("var g3 := (x1 + 3)^2 + (x2 + 3)^2 - 4")
        equations.append("gsys := min(max(g1, g2), g3) ")
        formula = ";".join(equations)
        limitStateFunction = ot.SymbolicFunction(["x1", "x2"], ["gsys"], formula)
        inputDimension = len(mu)
        if inputDimension != 2:
            raise Exception(
                "The dimension of mu is %d, but the expected dimension is 2."
                % (inputDimension)
            )

        inputDimension = len(sigma)
        if inputDimension != 2:
            raise Exception(
                "The dimension of sigma is %d, but the expected dimension is 2."
                % (inputDimension)
            )
        X1 = ot.Normal(mu[0], sigma[0])
        X1.setDescription(["X1"])
        X2 = ot.Normal(mu[1], sigma[1])
        X2.setDescription(["X2"])

        myDistribution = ot.ComposedDistribution([X1, X2])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP57"
        probability = 0.0284
        super(ReliabilityProblem57, self).__init__(name, thresholdEvent, probability)
        return None
