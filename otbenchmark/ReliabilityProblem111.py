# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:05:01 2020

@author: Jebroun

Class to define the ReliabilityProblem111 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem111(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, mu=[0.0] * 2, sigma=[1.0] * 2):
        """
        Creates a reliability problem RP111.

        The event is {g(X) < threshold} where

        g(x1, x2) = 12.5 - abs(x1 * x2)

        We have x1 ~ Normal(mu[0], sigma[0]) and x2 ~ Normal(mu[1], sigma[1]).

        Parameters
        ----------
        threshold : float
            The threshold.
        mu[0] : float
            The mean of the X1 gaussian distribution.
        sigma[0] : float
            The standard deviation of the X1 gaussian distribution.
        mu[1] : float
            The mean of the X2 gaussian distribution.
        sigma[1] : float
            The standard deviation of the X2 gaussian distribution.
        """
        formula = "12.5 - abs(x1 * x2)"
        limitStateFunction = ot.SymbolicFunction(["x1", "x2"], [formula])
        print(formula)

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

        name = "RP111"
        probability = 7.65e-7
        super(ReliabilityProblem111, self).__init__(name, thresholdEvent, probability)
        return None
