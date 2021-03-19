# -*- coding: utf-8 -*-
"""
Created on Tue May  5 12:56:49 2020

@author: Jebroun

Class to define the ReliabilityProblem60 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem60(ReliabilityBenchmarkProblem):
    def __init__(
        self,
        threshold=0.0,
        mu1=2200,
        sigma1=220,
        mu2=2100,
        sigma2=210,
        mu3=2300,
        sigma3=230,
        mu4=2000,
        sigma4=200,
        mu5=1200,
        sigma5=480,
    ):
        """
        Creates a reliability problem RP60.

        The event is {g(X) < threshold} with:

            X = (x1, x2, x3, x4, x5)

            g1 = x1 - x5

            g2 = x2 - x5 / 2

            g3 = x3 - x5 / 2

            g4 = x4 - x5 / 2

            g5 = x2 - x5

            g6 = x3 - x5

            g7 = x4 - x5

            g8 = min(g5, g6)

            g9 = max(g7, g8)

            g10 = min(g2, g3, g4)

            g11 = max(g10, g9)

            g(X) = min(g1, g11)

        We have :
            x1 ~ LogNormalMuSigma(mu1, sigma1)

            x2 ~ LogNormalMuSigma(mu2, sigma2)

            x3 ~ LogNormalMuSigma(mu3, sigma3)

            x4 ~ LogNormalMuSigma(mu4, sigma4)

            x5 ~ LogNormalMuSigma(mu5, sigma5)

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
        """
        equations = ["var g1 := x1 - x5"]
        equations.append("var g2 := x2 - x5 / 2")
        equations.append("var g3 := x3 - x5 / 2")
        equations.append("var g4 := x4 - x5 / 2")
        equations.append("var g5 := x2 - x5")
        equations.append("var g6 := x3 - x5")
        equations.append("var g7 := x4 - x5")
        equations.append("var g8 := min(g5, g6)")
        equations.append("var g9 := max(g7, g8)")
        equations.append("var g10 := min(g2, g3, g4)")
        equations.append("var g11 := max(g10, g9)")
        equations.append("gsys := min(g1, g11)")
        formula = ";".join(equations)
        limitStateFunction = ot.SymbolicFunction(
            ["x1", "x2", "x3", "x4", "x5"], ["gsys"], formula
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

        myDistribution = ot.ComposedDistribution([X1, X2, X3, X4, X5])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP60"
        probability = 0.0456
        super(ReliabilityProblem60, self).__init__(name, thresholdEvent, probability)
        return None
