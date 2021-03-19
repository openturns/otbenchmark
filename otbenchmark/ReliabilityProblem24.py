# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:18:59 2020

@author: Jebroun

Class to define the ReliabilityProblem24 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem24(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, mu=[10.0] * 2, sigma=[3.0] * 2):
        """
        Creates a reliability problem RP24.

        The event is {g(X) < threshold} where

        g(x1, x2) = 2.5 - 0.2357 * (x1 - x2) + 0.00463 * (x1 + x2 - 20)^4

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
        formula = "2.5 - 0.2357 * (x1 - x2) + 0.00463 * (x1 + x2 - 20)^4"
        limitStateFunction = ot.SymbolicFunction(["x1", "x2"], [formula])
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

        name = "RP24"

        probability = 0.00286
        super(ReliabilityProblem24, self).__init__(name, thresholdEvent, probability)
        return None
