"""Class to define the R-S benchmark problem."""

from ._ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class RminusSReliability(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, muR=4.0, sigmaR=1.0, muS=2.0, sigmaS=1.0):
        """
        Create a R-S reliability problem.

        The event is {g(X) < threshold} where

        g(R, S) = R - S

        We have R ~ Normal(muR, sigmaR) and S ~ Normal(muS, sigmaS).

        Waarts (2000) uses muR = 7.0 and muS = 2.0 leading to
        beta = 3.54.

        Parameters
        ----------
        threshold : float
            The threshold.

        muR : float
            The mean of the R gaussian distribution.

        sigmaR : float
            The standard deviation of the R gaussian distribution.

        muS : float
            The mean of the S gaussian distribution.

        sigmaS : float
            The standard deviation of the S gaussian distribution.

        Examples
        --------
        >>> import otbenchmark as otb
        >>> problem = otb.RminusSReliability()
        """
        limitStateFunction = ot.SymbolicFunction(["R", "S"], ["R - S"])

        R = ot.Normal(muR, sigmaR)
        R.setDescription("R")

        S = ot.Normal(muS, sigmaS)
        S.setDescription("S")

        myDistribution = ot.ComposedDistribution([R, S])

        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "R-S"
        diff = R - S
        probability = diff.computeCDF(threshold)
        super(RminusSReliability, self).__init__(name, thresholdEvent, probability)

        return None
