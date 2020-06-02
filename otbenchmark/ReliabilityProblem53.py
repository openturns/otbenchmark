"""
Youssef Jebroun
EDF

Class to define the ReliabilityProblem53 benchmark problem.

Created on Thu Apr 23 12:39:59 2020

@author: Jebroun

"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem53(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, mu1=1.5, sigma1=1.0, mu2=2.5, sigma2=1.0):
        """
        Creates a reliability problem RP53.

        The event is {g(X) < threshold} where

        g(X1, X2) = sin(5 * X1 / 2) + 2 - (X1^2 + 4) * (X2 - 1) / 20

        We have X1 ~ Normal(mu1, sigma1) and X2 ~ Normal(mu2, sigma2).

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
        formula = "sin(5 * x1 / 2) + 2 - ( x1 * x1 + 4 ) * ( x2 - 1 ) / 20"
        limitStateFunction = ot.SymbolicFunction(["x1", "x2"], [formula])

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

        name = "RP53"
        probability = 0.0313
        super(ReliabilityProblem53, self).__init__(name, thresholdEvent, probability)
        return None
