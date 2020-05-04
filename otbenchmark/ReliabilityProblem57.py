# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 10:52:22 2020

@author: Jebroun
Class to define the ReliabilityProblem57 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem57(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, mu1=0.0, sigma1=1.0, mu2=0.0, sigma2=1.0):
        """
        Creates a reliability problem RP57.

        The event is {g(X) < threshold} where
        g(x1, x2) = min(max(g1, g2), g3) with
        g1 = -x1^2 + x2^3 + 3
        g2 = 2 - x1 - 8 * x2
        g3 = (x1 + 3)^2 + (x2 + 3)^2 - 4
        We have x1 ~ Normal(mu1, sigma1) and x2 ~ Normal(mu2, sigma2).
        ***
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
        """
        equations = ["var g1 := -x1^2 + x2^3 + 3"]
        equations.append("var g2 := 2 - x1 - 8 * x2")
        equations.append("var g3 := (x1 + 3)^2 + (x2 + 3)^2 - 4")
        equations.append("gsys := min(max(g1, g2), g3) ")
        formula = ";".join(equations)
        limitStateFunction = ot.SymbolicFunction(["x1", "x2"], ["gsys"], formula)
        print(formula)
        X1 = ot.Normal(mu1, sigma1)
        X1.setDescription(["X1"])
        X2 = ot.Normal(mu2, sigma2)
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
