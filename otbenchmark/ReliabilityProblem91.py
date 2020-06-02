# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 10:58:25 2020

@author: Jebroun

Class to define the ReliabilityProblem91 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem91(ReliabilityBenchmarkProblem):
    def __init__(
        self,
        threshold=0.0,
        mu1=0.07433,
        sigma1=0.005,
        mu2=0.1,
        sigma2=0.01,
        mu3=13.0,
        sigma3=60.0,
        mu4=4751.0,
        sigma4=48.0,
        mu5=-684.0,
        sigma5=11.0,
    ):
        """
        Creates a reliability problem RP91.

        The event is {g(X) < threshold} where

        X = (x1, x2, x3, x4, x5)

        g1 = 0.847 + 0.96 * x2 + 0.986 * x3- 0.216 * x4 + 0.077 * x2^2 + 0.11
        * x3^2 + (7 / 378) * x4^2- x3 * x2 - 0.106 * x2 * x4 - 0.11 * x3 * x4

        g2 = 84000 * x1 / sqrt(x3^2 + x4^2 - x3 * x4 + 3 * x5^2) - 1

        g3 = 84000 * x1 / abs(x4) - 1

        g(X) = min(g1, g2, g3)

        We have :
            x1 ~ Normal(mu1, sigma1)

            x2 ~ Normal(mu2, sigma2)

            x3 ~ Normal(mu3, sigma3)

            x4 ~ Normal(mu4, sigma4)

            x5 ~ Normal(mu5, sigma5)

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
        mu4 : float
            The mean of the X4 gaussian distribution.
        sigma4 : float
            The standard deviation of the X4 gaussian distribution.
        mu5 : float
            The mean of the X5 gaussian distribution.
        sigma5 : float
            The standard deviation of the X5 gaussian distribution.
        """
        s = "0.847 + 0.96 * x2 + 0.986 * x3"
        s += "- 0.216 * x4 + 0.077 * x2^2 + "
        s += "0.11 * x3^2 + (7 / 378) * x4^2 "
        s += "- x3 * x2 - 0.106 * x2 * x4 - 0.11 * x3 * x4"

        equations = ["var g1 := " + s]
        equations.append(
            "var g2 := 84000 * x1 / sqrt(x3^2 + x4^2 - x3 * x4 + 3 * x5^2) - 1"
        )
        equations.append("var g3 := 84000 * x1 / abs(x4) - 1")
        equations.append("gsys := min(g1, g2, g3)")
        formula = ";".join(equations)
        limitStateFunction = ot.SymbolicFunction(
            ["x1", "x2", "x3", "x4", "x5"], ["gsys"], formula
        )
        X1 = ot.Normal(mu1, sigma1)
        X1.setDescription(["X1"])
        X2 = ot.Normal(mu2, sigma2)
        X2.setDescription(["X2"])
        X3 = ot.Normal(mu3, sigma3)
        X3.setDescription(["X3"])
        X4 = ot.Normal(mu4, sigma4)
        X4.setDescription(["X4"])
        X5 = ot.Normal(mu5, sigma5)
        X5.setDescription(["X5"])

        myDistribution = ot.ComposedDistribution([X1, X2, X3, X4, X5])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP91"
        probability = 0.000697
        super(ReliabilityProblem91, self).__init__(name, thresholdEvent, probability)
        return None
