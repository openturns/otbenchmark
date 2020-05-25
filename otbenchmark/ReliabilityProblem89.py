# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:39:49 2020

@author: Jebroun

Class to define the ReliabilityProblem89 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem89(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, mu=[0.0] * 2, sigma=[1.0] * 2):
        """
        Creates a reliability problem RP89.

        The event is {g(X) < threshold} where

        g(x1, x2) = min(-x1^2 - x2 + 8, -x1 / 5 - x2 + 6)

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
        equations = ["var g1 := -x1^2 - x2 + 8"]
        equations.append("var g2 := -x1 / 5 - x2 + 6")
        equations.append("gsys := min(g1, g2)")
        formula = ";".join(equations)
        limitStateFunction = ot.SymbolicFunction(["x1", "x2"], ["gsys"], formula)
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

        name = "RP89"
        probability = 0.00543
        super(ReliabilityProblem89, self).__init__(name, thresholdEvent, probability)
        return None
