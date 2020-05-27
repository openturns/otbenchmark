# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:58:15 2020

@author: Jebroun

Class to define the ReliabilityProblem77 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem77(ReliabilityBenchmarkProblem):
    def __init__(
        self,
        threshold=0.0,
        mu1=10.0,
        sigma1=0.5,
        mu2=0.0,
        sigma2=1.0,
        mu3=4.0,
        sigma3=1.0,
    ):
        """
        Creates a reliability problem RP77.

        The event is {g(X) < threshold} where

        X = (x1, x2, x3)

        if (x3 <= 5.0):
            g(x1, x2, x3) = x1 - x2 - x3

        else :
            g(x1, x2, x3) = x3 - x2

        We have :
            x1 ~ Normal(mu1, sigma1)

            x2 ~ Normal(mu2, sigma2)

            x3 ~ Normal(mu3, sigma3)

        Parameters
        ----------
        threshold : float
            The threshold.
        mu1 : float
            The mean of the X1 gaussian distribution.
        sigma1 : float
            The standard deviation of the X1 gaussian distribution.
        mu2 : float
            The mean of the X2 gaussian distribution.
        sigma2 : float
            The standard deviation of the X2 gaussian distribution.
        mu3 : float
            The mean of the X3 gaussian distribution.
        sigma3 : float
            The standard deviation of the X3 gaussian distribution.
        """
        equations = [
            "if (x3 <= 5.0)",
            "var g1 := x1 - x2 - x3;",
            "else",
            "  g1 := x3 - x2;",
            "gsys := g1;",
        ]
        program = "\n".join(equations)

        limitStateFunction = ot.SymbolicFunction(["x1", "x2", "x3"], ["gsys"], program)
        X1 = ot.Normal(mu1, sigma1)
        X1.setDescription(["X1"])
        X2 = ot.Normal(mu2, sigma2)
        X2.setDescription(["X2"])
        X3 = ot.Normal(mu3, sigma3)
        X3.setDescription(["X3"])

        myDistribution = ot.ComposedDistribution([X1, X2, X3])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP77"
        probability = 0.000000287
        super(ReliabilityProblem77, self).__init__(name, thresholdEvent, probability)
        return None
