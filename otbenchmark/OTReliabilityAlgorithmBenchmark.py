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


class OTReliabilityAlgorithmBenchmark:
    def FORM(
        problem,
        nearestPointAlgo="AbdoRackwitz",
        maximumEvaluationNumber=100,
        maximumAbsoluteError=1.0e-3,
        maximumRelativeError=1.0e-3,
        maximumResidualError=1.0e-3,
        maximumConstraintError=1.0e-3,
    ):
        """Runs the FORM algorithm and get the results."""
        if nearestPointAlgo == "AbdoRackwitz":
            nearestPointAlgorithm = ot.AbdoRackwitz()
        elif nearestPointAlgo == "Cobyla":
            nearestPointAlgorithm = ot.Cobyla()
        elif nearestPointAlgo == "SQP":
            nearestPointAlgorithm = ot.SQP()
        else:
            raise NameError(
                "Nearest point algorithm name must be \
                            'AbdoRackwitz', 'Cobyla' or 'SQP'."
            )
        nearestPointAlgorithm.setMaximumEvaluationNumber(maximumEvaluationNumber)
        nearestPointAlgorithm.setMaximumAbsoluteError(maximumAbsoluteError)
        nearestPointAlgorithm.setMaximumRelativeError(maximumRelativeError)
        nearestPointAlgorithm.setMaximumResidualError(maximumResidualError)
        nearestPointAlgorithm.setMaximumConstraintError(maximumConstraintError)
        algo = otb.FORM(problem, nearestPointAlgorithm)
        event = problem.getEvent()
        g = event.getFunction()
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algo.run()
        resultFORM = algo.getResult()
        numberOfFunctionEvaluationsFORM = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        computedProbability = resultFORM.getEventProbability()
        pfReference = problem.getProbability()
        absoluteError = abs(computedProbability - pfReference)
        numberOfCorrectDigits = otb.ComputeLogRelativeError(
            pfReference, computedProbability
        )

        return [
            computedProbability,
            absoluteError,
            numberOfCorrectDigits,
            numberOfFunctionEvaluationsFORM,
        ]

    def printResultFORM(benchmarkFORM):
        s = (
            "computedProbability = %s  "
            "absoluteError = %s "
            "numberOfCorrectDigits = %s "
            "numberOfFunctionEvaluations = %s"
        ) % (benchmarkFORM[0], benchmarkFORM[1], benchmarkFORM[2], benchmarkFORM[3],)
        return s

    def SORM(
        problem,
        nearestPointAlgo="AbdoRackwitz",
        maximumEvaluationNumber=100,
        maximumAbsoluteError=1.0e-3,
        maximumRelativeError=1.0e-3,
        maximumResidualError=1.0e-3,
        maximumConstraintError=1.0e-3,
    ):
        """Runs the SORM algorithm and get the results."""
        event = problem.getEvent()
        g = event.getFunction()
        initialNumberOfCall = g.getEvaluationCallsNumber()
        if nearestPointAlgo == "AbdoRackwitz":
            nearestPointAlgorithm = ot.AbdoRackwitz()
        elif nearestPointAlgo == "Cobyla":
            nearestPointAlgorithm = ot.Cobyla()
        elif nearestPointAlgo == "SQP":
            nearestPointAlgorithm = ot.SQP()
        else:
            raise NameError(
                "Nearest point algorithm name must be \
                            'AbdoRackwitz', 'Cobyla' or 'SQP'."
            )
        nearestPointAlgorithm.setMaximumEvaluationNumber(maximumEvaluationNumber)
        nearestPointAlgorithm.setMaximumAbsoluteError(maximumAbsoluteError)
        nearestPointAlgorithm.setMaximumRelativeError(maximumRelativeError)
        nearestPointAlgorithm.setMaximumResidualError(maximumResidualError)
        nearestPointAlgorithm.setMaximumConstraintError(maximumConstraintError)
        algo = otb.SORM(problem, nearestPointAlgorithm)
        algo.run()
        resultSORM = algo.getResult()
        numberOfFunctionEvaluationsSORM = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        computedProbability = resultSORM.getEventProbabilityBreitung()
        pfReference = problem.getProbability()
        absoluteError = abs(computedProbability - pfReference)
        numberOfCorrectDigits = otb.ComputeLogRelativeError(
            pfReference, computedProbability
        )
        return [
            computedProbability,
            absoluteError,
            numberOfCorrectDigits,
            numberOfFunctionEvaluationsSORM,
        ]

    def printResultSORM(benchmarkSORM):
        s = (
            "computedProbability = %s  "
            "absoluteError = %s "
            "numberOfCorrectDigits = %s "
            "numberOfFunctionEvaluations = %s"
        ) % (benchmarkSORM[0], benchmarkSORM[1], benchmarkSORM[2], benchmarkSORM[3],)
        return s

    def MonteCarloSampling(
        problem, maximumOuterSampling=1000, coefficientOfVariation=0.1, blockSize=1
    ):
        """
        Runs the ProbabilitySimulationAlgorithm with Monte-Carlo experiment
        algorithm and get results.
        """
        event = problem.getEvent()
        g = event.getFunction()
        factory = otb.ProbabilitySimulationAlgorithmFactory()
        algo = factory.buildMonteCarlo(problem)
        algo.setMaximumOuterSampling(maximumOuterSampling)
        algo.setBlockSize(blockSize)
        algo.setMaximumCoefficientOfVariation(coefficientOfVariation)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algo.run()
        resultMC = algo.getResult()
        numberOfFunctionEvaluationsMonteCarlo = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        graph = algo.drawProbabilityConvergence()
        computedProbability = resultMC.getProbabilityEstimate()
        pfReference = problem.getProbability()
        absoluteError = abs(computedProbability - pfReference)
        numberOfCorrectDigits = otb.ComputeLogRelativeError(
            pfReference, computedProbability
        )
        return [
            computedProbability,
            absoluteError,
            numberOfCorrectDigits,
            numberOfFunctionEvaluationsMonteCarlo,
            graph,
        ]

    def printResultMC(benchmarkMC):
        s = (
            "computedProbability = %s  "
            "absoluteError = %s "
            "numberOfCorrectDigits = %s "
            "numberOfFunctionEvaluations = %s"
        ) % (benchmarkMC[0], benchmarkMC[1], benchmarkMC[2], benchmarkMC[3],)
        return s

    def FORMImportanceSampling(
        problem,
        nearestPointAlgo="AbdoRackwitz",
        maximumEvaluationNumber=100,
        maximumAbsoluteError=1.0e-3,
        maximumRelativeError=1.0e-3,
        maximumResidualError=1.0e-3,
        maximumConstraintError=1.0e-3,
        maximumOuterSampling=5000,
        coefficientOfVariation=0.1,
    ):
        """
        Runs the Importance Sampling method with FORM importance
        distribution and get the number of function evaluations.
        """
        if nearestPointAlgo == "AbdoRackwitz":
            nearestPointAlgorithm = ot.AbdoRackwitz()
        elif nearestPointAlgo == "Cobyla":
            nearestPointAlgorithm = ot.Cobyla()
        elif nearestPointAlgo == "SQP":
            nearestPointAlgorithm = ot.SQP()
        else:
            raise NameError(
                "Nearest point algorithm name must be \
                            'AbdoRackwitz', 'Cobyla' or 'SQP'."
            )
        nearestPointAlgorithm.setMaximumEvaluationNumber(maximumEvaluationNumber)
        nearestPointAlgorithm.setMaximumAbsoluteError(maximumAbsoluteError)
        nearestPointAlgorithm.setMaximumRelativeError(maximumRelativeError)
        nearestPointAlgorithm.setMaximumResidualError(maximumResidualError)
        nearestPointAlgorithm.setMaximumConstraintError(maximumConstraintError)
        factory = otb.ProbabilitySimulationAlgorithmFactory()
        algo = factory.buildFORMIS(problem, nearestPointAlgorithm)
        event = problem.getEvent()
        g = event.getFunction()
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algo.setMaximumCoefficientOfVariation(coefficientOfVariation)
        algo.setMaximumOuterSampling(maximumOuterSampling)
        algo.setConvergenceStrategy(ot.Full())
        algo.run()
        result = algo.getResult()
        graph = algo.drawProbabilityConvergence()
        numberOfFunctionEvaluationsFORMIS = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        computedProbability = result.getProbabilityEstimate()
        pfReference = problem.getProbability()
        absoluteError = abs(computedProbability - pfReference)
        numberOfCorrectDigits = otb.ComputeLogRelativeError(
            pfReference, computedProbability
        )

        return [
            computedProbability,
            absoluteError,
            numberOfCorrectDigits,
            numberOfFunctionEvaluationsFORMIS,
            graph,
        ]

    def printResultFORMIS(benchmarFORMIS):
        s = (
            "computedProbability = %s  "
            "absoluteError = %s "
            "numberOfCorrectDigits = %s "
            "numberOfFunctionEvaluations = %s"
        ) % (
            benchmarFORMIS[0],
            benchmarFORMIS[1],
            benchmarFORMIS[2],
            benchmarFORMIS[3],
        )
        return s

    def SubsetSampling(
        problem, maximumOuterSampling=5000, coefficientOfVariation=0.1, blockSize=1
    ):
        """
        Runs the Subset method and get the results.
        """
        event = problem.getEvent()
        g = event.getFunction()
        algo = otb.SubsetSampling(problem)
        algo.setMaximumOuterSampling(maximumOuterSampling)
        algo.setMaximumCoefficientOfVariation(coefficientOfVariation)
        algo.setBlockSize(blockSize)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algo.run()
        graph = algo.drawProbabilityConvergence()
        resultSS = algo.getResult()
        computedProbability = resultSS.getProbabilityEstimate()
        pfReference = problem.getProbability()
        absoluteError = abs(computedProbability - pfReference)
        numberOfCorrectDigits = otb.ComputeLogRelativeError(
            pfReference, computedProbability
        )
        numberOfFunctionEvaluationsSS = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        return [
            computedProbability,
            absoluteError,
            numberOfCorrectDigits,
            numberOfFunctionEvaluationsSS,
            graph,
        ]

    def printResultSubset(benchmarkSS):
        s = (
            "computedProbability = %s  "
            "absoluteError = %s "
            "numberOfCorrectDigits = %s "
            "numberOfFunctionEvaluations = %s"
        ) % (benchmarkSS[0], benchmarkSS[1], benchmarkSS[2], benchmarkSS[3],)
        return s

    def LHS(
        problem, maximumOuterSampling=1000, coefficientOfVariation=0.1, blockSize=1
    ):
        """Runs the LHS algorithm and get the results."""
        event = problem.getEvent()
        g = event.getFunction()
        algo = otb.LHS(problem)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algo.setMaximumCoefficientOfVariation(0.05)
        algo.setMaximumOuterSampling(int(1.0e5))
        algo.run()
        numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
        result = algo.getResult()
        graph = algo.drawProbabilityConvergence()
        computedProbability = result.getProbabilityEstimate()
        pfReference = problem.getProbability()
        absoluteError = abs(computedProbability - pfReference)
        numberOfCorrectDigits = otb.ComputeLogRelativeError(
            pfReference, computedProbability
        )
        return [
            computedProbability,
            absoluteError,
            numberOfCorrectDigits,
            numberOfFunctionEvaluations,
            graph,
        ]
