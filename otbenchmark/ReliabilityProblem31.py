# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 12:32:41 2020

@author: Jebroun

Class to define the ReliabilityProblem31 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem31(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, mu1=0.0, sigma1=1.0, mu2=0.0, sigma2=1.0):
        """
        Creates a reliability problem RP31.

        The event is {g(X) < threshold} where
        g(x1, x2) = 2 - x2 + 256 * x1^4
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
        formula = "2 - x2 + 256 * x1^4"
        limitStateFunction = ot.SymbolicFunction(["x1", "x2"], [formula])
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

        name = "RP31"
        probability = 0.00018
        super(ReliabilityProblem31, self).__init__(name, thresholdEvent, probability)
        return None
