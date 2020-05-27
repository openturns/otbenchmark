# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:26:53 2020

@author: Jebroun

Class to define the ReliabilityProblem8 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem8(ReliabilityBenchmarkProblem):
    def __init__(
        self,
        threshold=0.0,
        mu1=120.0,
        sigma1=12.0,
        mu2=120.0,
        sigma2=12.0,
        mu3=120.0,
        sigma3=12.0,
        mu4=120.0,
        sigma4=12.0,
        mu5=50.0,
        sigma5=10.0,
        mu6=40.0,
        sigma6=8.0,
    ):
        """
        Creates a reliability problem RP8.

        The event is {g(X) < threshold} where

        X = (x1, x2, x3, x4, x5, x6)

        g(X) = x1 + 2 * x2 + 2 * x3 + x4 - 5 * x5 - 5 * x6

        We have :
            x1 ~ LogNormalMuSigma(mu1, sigma1)

            x2 ~ LogNormalMuSigma(mu2, sigma2)

            x3 ~ LogNormalMuSigma(mu3, sigma3)

            x4 ~ LogNormalMuSigma(mu4, sigma4)

            x5 ~ LogNormalMuSigma(mu5, sigma5)

            x6 ~ LogNormalMuSigma(mu6, sigma6)

        Parameters
        ----------
        threshold : float
            The threshold.
        mu1 : float
            The mean of the LogNormal random variable X1.
        sigma1 : float
            The standard deviation of the LogNormal random variable X1.
        mu2 : float
            The mean of the LogNormal random variable X2.
        sigma2 : float
            The standard deviation of the LogNormal random variable X2.
        mu3 : float
            The mean of the LogNormal random variable X3.
        sigma3 : float
            The standard deviation of the LogNormal random variable X3.
        mu4 : float
            The mean of the LogNormal random variable X4.
        sigma4 : float
            The standard deviation of the LogNormal random variable X4.
        mu5 : float
            The mean of the LogNormal random variable X5.
        sigma5 : float
            The standard deviation of the LogNormal random variable X5.
        mu6 : float
            The mean of the LogNormal random variable X6.
        sigma6 : float
            The standard deviation of the LogNormal random variable X6.
        """

        formula = "x1 + 2 * x2 + 2 * x3 + x4 - 5 * x5 - 5 * x6"

        limitStateFunction = ot.SymbolicFunction(
            ["x1", "x2", "x3", "x4", "x5", "x6"], [formula]
        )
        parameters1 = ot.LogNormalMuSigma(mu1, sigma1, 0.0)
        X1 = ot.ParametrizedDistribution(parameters1)
        X1.setDescription(["X1"])
        parameters2 = ot.LogNormalMuSigma(mu2, sigma2, 0.0)
        X2 = ot.ParametrizedDistribution(parameters2)
        X2.setDescription(["X2"])
        parameters3 = ot.LogNormalMuSigma(mu3, sigma3, 0.0)
        X3 = ot.ParametrizedDistribution(parameters3)
        X3.setDescription(["X3"])
        parameters4 = ot.LogNormalMuSigma(mu4, sigma4, 0.0)
        X4 = ot.ParametrizedDistribution(parameters4)
        X4.setDescription(["X4"])
        parameters5 = ot.LogNormalMuSigma(mu5, sigma5, 0.0)
        X5 = ot.ParametrizedDistribution(parameters5)
        X5.setDescription(["X5"])
        parameters6 = ot.LogNormalMuSigma(mu6, sigma6, 0.0)
        X6 = ot.ParametrizedDistribution(parameters6)
        X6.setDescription(["X6"])

        myDistribution = ot.ComposedDistribution([X1, X2, X3, X4, X5, X6])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP8"
        probability = 0.000784
        super(ReliabilityProblem8, self).__init__(name, thresholdEvent, probability)
        return None
