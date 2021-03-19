# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:50:49 2020

@author: Jebroun


Class to define the ReliabilityProblem14 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem14(ReliabilityBenchmarkProblem):
    def __init__(
        self,
        threshold=0.0,
        a=70.0,
        b=80.0,
        mu2=39.0,
        sigma2=0.1,
        mu3=1500.0,
        sigma3=350.0,
        mu4=400.0,
        sigma4=0.1,
        mu5=250000.0,
        sigma5=35000.0,
    ):
        """
        Creates a reliability problem RP14.

        The event is {g(X) < threshold} where

        X = (x1, x2, x3, x4, x5)

        g(X) = x1 - 32 / (pi_ * x2^3) * sqrt(x3^2 * x4^2 / 16 + x5^2)

        We have :
            x1 ~ Uniform(a, b)

            x2 ~ Normal(mu2, sigma2)

            x3 ~ Gumbel-max(mu3, sigma3)

            x4 ~ Normal(mu4, sigma4)

            x5 ~ Normal(mu5, sigma5)

        Parameters
        ----------
        threshold : float
            The threshold.
        a : float
            Lower bound of the Uniform distribution X1.
        b : float
            Upper bound of the Uniform distribution X1.
        mu2 : float
            The mean of the X2 Normal distribution.
        sigma2 : float
            The standard deviation of the X2 Normal distribution.
        mu3 : float
            The mean of the X3 Gumbel distribution.
        sigma3 : float
            The standard deviation of the X3 Gumbel distribution.
        mu4 : float
            The mean of the X4 Normal distribution.
        sigma4 : float
            The standard deviation of the X4 Normal distribution.
        mu5 : float
            The mean of the X5 Normal distribution.
        sigma5 : float
            The standard deviation of the X5 Normal distribution.
        """

        formula = "x1 - 32 / (pi_ * x2^3) * sqrt(x3^2 * x4^2 / 16 + x5^2)"

        limitStateFunction = ot.SymbolicFunction(
            ["x1", "x2", "x3", "x4", "x5"], [formula]
        )
        X1 = ot.Uniform(a, b)
        X1.setDescription(["X1"])
        X2 = ot.Normal(mu2, sigma2)
        X2.setDescription(["X2"])
        X3 = ot.ParametrizedDistribution(ot.GumbelMuSigma(mu3, sigma3))
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

        name = "RP14"
        probability = 0.00752
        super(ReliabilityProblem14, self).__init__(name, thresholdEvent, probability)
        return None
