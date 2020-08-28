# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 11:37:47 2020

@author: Jebroun
"""
import openturns as ot
import otbenchmark as otb
import numpy as np

"""
Static methods to create a list of all reliability problems.
"""


def ComputeLogRelativeError(exact, computed, basis=10.0):
    """
    Compute the log-relative error between exact and computed.

    The log-relative error (LRE) is defined by:

        LRE = -logB(relativeError)

    where relativeError is the relative error:

        relativeError = abs(exact - computed) / abs(exact)

    and logB is the base-b logarithm:

        logB(x) = log(x) / log(basis)

    where log is the natural logarithm.
    This assumes that exact is different from zero.

    The LRE is the number of base-B common digits in exact and computed.

    Parameters
    ----------
    exact: float
        The exact value.
    computed: float
        The computed value.

    Returns
    -------
    logRelativeError: float
        The LRE.
    """
    relativeError = abs(exact - computed) / abs(exact)
    logRelativeError = -np.log(relativeError) / np.log(basis)
    return logRelativeError


def ComputeAbsoluteError(exact, computed):
    """
    Compute absolute error between exact and computed.

    The absolute error is defined by:

        absoluteError = abs(exact - computed).

    Parameters
    ----------
    exact: float
        The exact value.
    computed: float
        The computed value.

    Returns
    -------
    absoluteError: float
        The absolute error.
    """
    absoluteError = abs(exact - computed)
    return absoluteError


def ComputeRelativeError(exact, computed):
    """
    Compute relative error between exact and computed.

    The relative error is defined by:

        relativeError = abs(exact - computed) / abs(exact)

    if exact is different from zero.

    Parameters
    ----------
    exact: float
        The exact value.
    computed: float
        The computed value.

    Returns
    -------
    relativeError: float
        The relative error.
    """
    relativeError = abs(exact - computed) / abs(exact)
    return relativeError


def ReliabilityBenchmarkProblemList():
    """
    Returns the list of reliability benchmark problems.

    Returns
    -------
    problemslist : list
        A list of ReliabilityProblem.
    """
    p8 = otb.ReliabilityProblem8()
    p14 = otb.ReliabilityProblem14()
    p22 = otb.ReliabilityProblem22()
    p24 = otb.ReliabilityProblem24()
    p25 = otb.ReliabilityProblem25()
    p28 = otb.ReliabilityProblem28()
    p31 = otb.ReliabilityProblem31()
    p33 = otb.ReliabilityProblem33()
    p35 = otb.ReliabilityProblem35()
    p38 = otb.ReliabilityProblem38()
    p53 = otb.ReliabilityProblem53()
    p55 = otb.ReliabilityProblem55()
    p54 = otb.ReliabilityProblem54()
    p57 = otb.ReliabilityProblem57()
    p75 = otb.ReliabilityProblem75()
    p89 = otb.ReliabilityProblem89()
    p107 = otb.ReliabilityProblem107()
    p110 = otb.ReliabilityProblem110()
    p111 = otb.ReliabilityProblem111()
    p63 = otb.ReliabilityProblem63()
    p91 = otb.ReliabilityProblem91()
    p60 = otb.ReliabilityProblem60()
    p77 = otb.ReliabilityProblem77()
    pFBS = otb.FourBranchSerialSystemReliability()
    pRS = otb.RminusSReliability()
    pBeam = otb.AxialStressedBeamReliability()
    problemslist = [
        p8,
        p14,
        p22,
        p24,
        p25,
        p28,
        p31,
        p33,
        p35,
        p38,
        p53,
        p55,
        p54,
        p57,
        p75,
        p89,
        p107,
        p110,
        p111,
        p63,
        p91,
        p60,
        p77,
        pFBS,
        pRS,
        pBeam,
    ]
    return problemslist


class ReliabilityBenchmarkMetaAlgorithm:
    def __init__(self, problem):
        """
        Create a meta-algorithm to solve a reliability problem.


        Parameters
        ----------
        problem : ot.ReliabilityBenchmarkProblem
            The problem.
        """
        #
        self.problem = problem
        return None

    def runFORM(self, nearestPointAlgorithm):
        """
        Runs the FORM algorithm and get the results.

        Parameters
        ----------
        nearestPointAlgorithm : ot.OptimizationAlgorithm
            Optimization algorithm used to search the design point.

        Returns
        -------
        result : ReliabilityBenchmarkResult
            The problem result.
        """
        algo = otb.FORM(self.problem, nearestPointAlgorithm)
        event = self.problem.getEvent()
        g = event.getFunction()
        initialNumberOfCall = g.getEvaluationCallsNumber()
        try:
            algo.run()
            resultFORM = algo.getResult()
            computedProbability = resultFORM.getEventProbability()
        except RuntimeError:
            computedProbability = 0.0
        numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
        pfReference = self.problem.getProbability()
        result = ReliabilityBenchmarkResult(
            pfReference, computedProbability, numberOfFunctionEvaluations
        )
        return result

    def runSORM(self, nearestPointAlgorithm):
        """
        Runs the SORM algorithm and get the results.

        Parameters
        ----------
        nearestPointAlgorithm : ot.OptimizationAlgorithm
            Optimization algorithm used to search the design point.

        Returns
        -------
        result : ReliabilityBenchmarkResult
            The problem result.
        """
        event = self.problem.getEvent()
        g = event.getFunction()
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algo = otb.SORM(self.problem, nearestPointAlgorithm)
        try:
            algo.run()
            resultSORM = algo.getResult()
            computedProbability = resultSORM.getEventProbabilityBreitung()
        except RuntimeError:
            computedProbability = 0.0
        numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
        pfReference = self.problem.getProbability()
        result = ReliabilityBenchmarkResult(
            pfReference, computedProbability, numberOfFunctionEvaluations
        )
        return result

    def runMonteCarlo(
        self, maximumOuterSampling=1000, coefficientOfVariation=0.1, blockSize=1
    ):
        """
        Runs the ProbabilitySimulationAlgorithm with Monte-Carlo experiment
        algorithm and get results.

        Parameters
        ----------
        maximumOuterSampling : int
            The maximum number of outer iterations.
        coefficientOfVariation : float
            The maximum coefficient of variation.
        blockSize : int
            The number of inner iterations.

        Returns
        -------
        result : ReliabilityBenchmarkResult
            The problem result.
        """
        event = self.problem.getEvent()
        g = event.getFunction()
        factory = otb.ProbabilitySimulationAlgorithmFactory()
        algo = factory.buildMonteCarlo(self.problem)
        algo.setMaximumOuterSampling(maximumOuterSampling)
        algo.setBlockSize(blockSize)
        algo.setMaximumCoefficientOfVariation(coefficientOfVariation)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algo.run()
        resultMC = algo.getResult()
        numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
        computedProbability = resultMC.getProbabilityEstimate()
        pfReference = self.problem.getProbability()
        result = ReliabilityBenchmarkResult(
            pfReference, computedProbability, numberOfFunctionEvaluations
        )
        return result

    def runFORMImportanceSampling(
        self,
        nearestPointAlgorithm,
        maximumOuterSampling=1000,
        coefficientOfVariation=0.1,
    ):
        """
        Runs the Importance Sampling method with FORM importance
        distribution and get the number of function evaluations.

        Parameters
        ----------
        nearestPointAlgorithm : ot.OptimizationAlgorithm
            Optimization algorithm used to search the design point.
        maximumOuterSampling : int
            The maximum number of outer iterations.
        coefficientOfVariation : float
            The maximum coefficient of variation.

        Returns
        -------
        result : ReliabilityBenchmarkResult
            The problem result.
        """
        factory = otb.ProbabilitySimulationAlgorithmFactory()
        event = self.problem.getEvent()
        g = event.getFunction()
        initialNumberOfCall = g.getEvaluationCallsNumber()
        try:
            algo = factory.buildFORMIS(self.problem, nearestPointAlgorithm)
            algo.setMaximumCoefficientOfVariation(coefficientOfVariation)
            algo.setMaximumOuterSampling(maximumOuterSampling)
            algo.setConvergenceStrategy(ot.Full())
            algo.run()
            result = algo.getResult()
            computedProbability = result.getProbabilityEstimate()
        except RuntimeError:
            computedProbability = 0.0
        numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
        pfReference = self.problem.getProbability()
        result = ReliabilityBenchmarkResult(
            pfReference, computedProbability, numberOfFunctionEvaluations
        )
        return result

    def runSubsetSampling(
        self, maximumOuterSampling=1000, coefficientOfVariation=0.1, blockSize=1
    ):
        """
        Runs the Subset method and get the results.

        Parameters
        ----------
        maximumOuterSampling : int
            The maximum number of outer iterations.
        coefficientOfVariation : float
            The maximum coefficient of variation.
        blockSize : int
            The number of inner iterations.

        Returns
        -------
        result : ReliabilityBenchmarkResult
            The problem result.
        """
        event = self.problem.getEvent()
        g = event.getFunction()
        algo = otb.SubsetSampling(self.problem)
        algo.setMaximumOuterSampling(maximumOuterSampling)
        algo.setMaximumCoefficientOfVariation(coefficientOfVariation)
        algo.setBlockSize(blockSize)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algo.run()
        resultSS = algo.getResult()
        computedProbability = resultSS.getProbabilityEstimate()
        pfReference = self.problem.getProbability()
        numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
        result = ReliabilityBenchmarkResult(
            pfReference, computedProbability, numberOfFunctionEvaluations
        )
        return result

    def runLHS(
        self, maximumOuterSampling=1000, coefficientOfVariation=0.1, blockSize=1
    ):
        """
        Runs the LHS algorithm and get the results.

        Parameters
        ----------
        maximumOuterSampling : int
            The maximum number of outer iterations.
        coefficientOfVariation : float
            The maximum coefficient of variation.
        blockSize : int
            The number of inner iterations.

        Returns
        -------
        result : ReliabilityBenchmarkResult
            The problem result.
        """
        event = self.problem.getEvent()
        g = event.getFunction()
        algo = otb.LHS(self.problem)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algo.setMaximumCoefficientOfVariation(coefficientOfVariation)
        algo.setMaximumOuterSampling(maximumOuterSampling)
        algo.run()
        numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
        result = algo.getResult()
        computedProbability = result.getProbabilityEstimate()
        pfReference = self.problem.getProbability()
        result = ReliabilityBenchmarkResult(
            pfReference, computedProbability, numberOfFunctionEvaluations
        )
        return result


class ReliabilityBenchmarkResult:
    def __init__(
        self, exactProbability, computedProbability, numberOfFunctionEvaluations
    ):
        """
        Create a benchmark result for a reliability problem.
        """
        self.computedProbability = computedProbability
        self.exactProbability = exactProbability
        absoluteError = abs(computedProbability - exactProbability)
        self.absoluteError = absoluteError
        numberOfCorrectDigits = otb.ComputeLogRelativeError(
            exactProbability, computedProbability
        )
        self.numberOfCorrectDigits = numberOfCorrectDigits
        self.numberOfFunctionEvaluations = numberOfFunctionEvaluations
        self.numberOfDigitsPerEvaluation = (
            self.numberOfCorrectDigits / self.numberOfFunctionEvaluations
        )
        return None

    def summary(self):
        s = (
            "computedProbability = %s  "
            "exactProbability = %s  "
            "absoluteError = %s "
            "numberOfCorrectDigits = %s "
            "numberOfFunctionEvaluations = %s"
            "numberOfDigitsPerEvaluation = %s"
        ) % (
            self.computedProbability,
            self.exactProbability,
            self.absoluteError,
            self.numberOfCorrectDigits,
            self.numberOfFunctionEvaluations,
            self.numberOfDigitsPerEvaluation,
        )
        return s
