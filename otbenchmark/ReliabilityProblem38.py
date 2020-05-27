# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 12:45:56 2020

@author: Jebroun


Class to define the ReliabilityProblem38 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem38(ReliabilityBenchmarkProblem):
    def __init__(
        self,
        threshold=0.0,
        mu1=350,
        sigma1=35,
        mu2=50.8,
        sigma2=5.08,
        mu3=3.81,
        sigma3=0.381,
        mu4=173,
        sigma4=17.3,
        mu5=9.38,
        sigma5=0.938,
        mu6=33.1,
        sigma6=3.31,
        mu7=0.036,
        sigma7=0.0036,
    ):
        """
        Creates a reliability problem RP38.

        The event is {g(X) < threshold} where

        X = (x1, x2, x3, x4, x5, x6, x7)

        g(X) = 15.59 * 1e4 - x1 *x2^3 / (2 * x3^3)
        * ((x4^2 - 4 * x5 * x6 * x7^2 +x4 * (x6 + 4 * x5 + 2 *x6 * x7))
        / (x4 * x5 * (x4 + x6 + 2 *x6 *x7)))

        We have :
            x1 ~ Normal(mu1, sigma1)

            x2 ~ Normal(mu2, sigma2)

            x3 ~ Normal(mu3, sigma3)

            x4 ~ Normal(mu4, sigma4)

            x5 ~ Normal(mu5, sigma5)

            x6 ~ Normal(mu6, sigma6)

            x7 ~ Normal(mu7, sigma7)

        Parameters
        ----------
        threshold : float
            The threshold.
        mu1 : float
            The mean of the X1 Normal distribution.
        sigma1 : float
            The standard deviation of the X1 Normal distribution.
        mu2 : float
            The mean of the X2 Normal distribution.
        sigma2 : float
            The standard deviation of the X2 Normal distribution.
        mu3 : float
            The mean of the X3 Normal distribution.
        sigma3 : float
            The standard deviation of the X3 Normal distribution.
        mu4 : float
            The mean of the X4 Normal distribution.
        sigma4 : float
            The standard deviation of the X4 Normal distribution.
        mu5 : float
            The mean of the X5 Normal distribution.
        sigma5 : float
            The standard deviation of the X5 Normal distribution.
        mu6 : float
            The mean of the X6 Normal distribution.
        sigma6 : float
            The standard deviation of the X6 Normal distribution.
        mu7 : float
            The mean of the X7 Normal distribution.
        sigma7 : float
            The standard deviation of the X7 Normal distribution.
        """

        formula = "15.59 * 1e4 - x1 *x2^3 / (2 * x3^3) *"
        formula += "((x4^2 - 4 * x5 * x6 * x7^2 + "
        formula += (
            "x4 * (x6 + 4 * x5 + 2 *x6 * x7)) / (x4 * x5 * (x4 + x6 + 2 *x6 *x7)))"
        )

        limitStateFunction = ot.SymbolicFunction(
            ["x1", "x2", "x3", "x4", "x5", "x6", "x7"], [formula]
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
        X6 = ot.Normal(mu6, sigma6)
        X6.setDescription(["X6"])
        X7 = ot.Normal(mu7, sigma7)
        X7.setDescription(["X7"])

        myDistribution = ot.ComposedDistribution([X1, X2, X3, X4, X5, X6, X7])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP38"
        probability = 0.0081
        super(ReliabilityProblem38, self).__init__(name, thresholdEvent, probability)
        return None
