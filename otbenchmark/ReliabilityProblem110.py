# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 11:05:38 2020

@author: Jebroun

Class to define the ReliabilityProblem110 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem110(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, mu=[0.0] * 2, sigma=[1.0] * 2):
        """
        Creates a reliability problem RP110.

        The event is {g(X) < threshold} where

        g(x1, x2) = min(g1, g2) with :

            if(x1 <= 3.5) :
                g1 = 0.85 - 0.1 * x1
            else :
                g1 = 4 - x1
            and

            if(x2 <= 2) :
                g2 = 2.3 - x2
            else :
                g2 = 0.5 - 0.1 * x2

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
        equations = [
            "if (x0 <= 3.5)",
            "var g1 := 0.85 - 0.1 * x0;",
            "else",
            "  g1 := 4 - x0;",
            "if (x1 <= 2.0)",
            "  var g2 := 2.3 - x1;",
            "else",
            "  g2 := 0.5 - 0.1 * x1;",
            "gsys := min(g1, g2);",
        ]
        program = "\n".join(equations)
        limitStateFunction = ot.SymbolicFunction(["x0", "x1"], ["gsys"], program)
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

        name = "RP110"
        probability = 0.0000319
        super(ReliabilityProblem110, self).__init__(name, thresholdEvent, probability)
        return None
