# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 11:05:38 2020

@author: Jebroun

Class to define the ReliabilityProblem110 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem110(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, mu1=0.0, sigma1=1.0, mu2=0.0, sigma2=1.0):
        """
        Creates a reliability problem RP110.

        The event is {g(X) < threshold} where
        g(x1, x2) = min(g1, g2) with :
            g1 = 0.85 - 0.1 * x1  if  x1 <= 3.5
            else
            g1 = 4 - x1
            and
            g2 = 2.3 - x2  if  x2 <= 2
            else
            g2 = 0.5 - 0.1 * x2
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
        print(program)
        limitStateFunction = ot.SymbolicFunction(["x0", "x1"], ["gsys"], program)
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

        name = "RP110"
        probability = 0.0000319
        super(ReliabilityProblem110, self).__init__(name, thresholdEvent, probability)
        return None
