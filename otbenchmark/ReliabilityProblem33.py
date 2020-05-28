# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 10:21:03 2020

@author: Jebroun

Class to define the ReliabilityProblem33 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem33(ReliabilityBenchmarkProblem):
    def __init__(
        self, threshold=0.0, mu=[0.0] * 3, sigma=[1.0] * 3,
    ):
        """
        Creates a reliability problem RP33.

        The event is {g(X) < threshold} where

        g(x1, x2, x3) = min(g1, g2) with

        g1 = -x1 - x2 - x3 + 3 * sqrt(3)

        g2 = -x3 + 3

        We have :
            x1 ~ Normal(mu[0], sigma[0])

            x2 ~ Normal(mu[1], sigma[1])

            x3 ~ Normal(mu[2], sigma[2]).

        Parameters
        ----------
        threshold : float
            The threshold.
        mu : sequence of floats
            The list of 3 items representing the means of the gaussian distributions.
        sigma : float
            The list of 3 items representing the standard deviations of
            the gaussian distributions.
        """
        formula = "min(-x1 - x2 - x3 + 3 * sqrt(3), -x3 + 3)"
        limitStateFunction = ot.SymbolicFunction(["x1", "x2", "x3"], [formula])
        inputDimension = len(mu)
        if inputDimension != 3:
            raise Exception(
                "The dimension of mu is %d, but the expected dimension is 3."
                % (inputDimension)
            )

        inputDimension = len(sigma)
        if inputDimension != 3:
            raise Exception(
                "The dimension of sigma is %d, but the expected dimension is 3."
                % (inputDimension)
            )
        X1 = ot.Normal(mu[0], sigma[0])
        X1.setDescription(["X1"])
        X2 = ot.Normal(mu[1], sigma[1])
        X2.setDescription(["X2"])
        X3 = ot.Normal(mu[2], sigma[2])
        X3.setDescription(["X3"])

        myDistribution = ot.ComposedDistribution([X1, X2, X3])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP33"
        probability = 0.00257
        super(ReliabilityProblem33, self).__init__(name, thresholdEvent, probability)
        return None
