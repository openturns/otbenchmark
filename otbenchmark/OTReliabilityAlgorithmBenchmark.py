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


def computeLogRelativeError(exact, computed):
    logRelativeError = -np.log10(abs(exact - computed) / abs(exact))
    return logRelativeError


class OTReliabilityAlgorithmBenchmark:
    def __init__(self):
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
        listProblems = [
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
        self.problemslist = listProblems
        return None

    def FORM(
        problem,
        nearestPointAlgo="AbdoRackwitz",
        maximumEvaluationNumber=100,
        maximumAbsoluteError=1.0e-3,
        maximumRelativeError=1.0e-3,
        maximumResidualError=1.0e-3,
        maximumConstraintError=1.0e-3,
    ):

        if nearestPointAlgo == "AbdoRackwitz":
            solver = ot.AbdoRackwitz()
        elif nearestPointAlgo == "Cobyla":
            solver = ot.Cobyla()
        elif nearestPointAlgo == "SQP":
            solver = ot.SQP()
        else:
            raise NameError(
                "Nearest point algorithm name must be \
                            'AbdoRackwitz', 'Cobyla' or 'SQP'."
            )

        solver.setMaximumEvaluationNumber(maximumEvaluationNumber)
        solver.setMaximumAbsoluteError(maximumAbsoluteError)
        solver.setMaximumRelativeError(maximumRelativeError)
        solver.setMaximumResidualError(maximumResidualError)
        solver.setMaximumConstraintError(maximumConstraintError)
        myEvent = problem.getEvent()
        inputVector = myEvent.getAntecedent()
        myDistribution = inputVector.getDistribution()
        g = problem.getEvent().getFunction()
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algoFORM = ot.FORM(solver, myEvent, myDistribution.getMean())
        algoFORM.run()
        resultFORM = algoFORM.getResult()
        numberOfFunctionEvaluationsFORM = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        probabilityEstime = resultFORM.getEventProbability()
        absolueError = abs(probabilityEstime - problem.getProbability())
        numberOfCorrectDigits = computeLogRelativeError(
            problem.getProbability(), probabilityEstime
        )

        return [
            probabilityEstime,
            absolueError,
            numberOfCorrectDigits,
            numberOfFunctionEvaluationsFORM,
        ]

    def SORM(
        problem,
        nearestPointAlgo="AbdoRackwitz",
        maximumEvaluationNumber=100,
        maximumAbsoluteError=1.0e-3,
        maximumRelativeError=1.0e-3,
        maximumResidualError=1.0e-3,
        maximumConstraintError=1.0e-3,
    ):
        if nearestPointAlgo == "AbdoRackwitz":
            solver = ot.AbdoRackwitz()
        elif nearestPointAlgo == "Cobyla":
            solver = ot.Cobyla()
        elif nearestPointAlgo == "SQP":
            solver = ot.SQP()
        else:
            raise NameError(
                "Nearest point algorithm name must be \
                            'AbdoRackwitz', 'Cobyla' or 'SQP'."
            )

        solver.setMaximumEvaluationNumber(maximumEvaluationNumber)
        solver.setMaximumAbsoluteError(maximumAbsoluteError)
        solver.setMaximumRelativeError(maximumRelativeError)
        solver.setMaximumResidualError(maximumResidualError)
        solver.setMaximumConstraintError(maximumConstraintError)

        myEvent = problem.getEvent()
        inputVector = myEvent.getAntecedent()
        myDistribution = inputVector.getDistribution()
        g = problem.getEvent().getFunction()
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algoSORM = ot.SORM(solver, myEvent, myDistribution.getMean())
        algoSORM.run()
        resultSORM = algoSORM.getResult()
        numberOfFunctionEvaluationsSORM = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        probabilityEstime = resultSORM.getEventProbabilityBreitung()
        absolueError = abs(probabilityEstime - problem.getProbability())
        numberOfCorrectDigits = computeLogRelativeError(
            problem.getProbability(), probabilityEstime
        )
        return [
            probabilityEstime,
            absolueError,
            numberOfCorrectDigits,
            numberOfFunctionEvaluationsSORM,
        ]

    def MonteCarloSampling(
        problem, maximumOuterSampling=1000, coefficientOfVariation=0.1, blockSize=1
    ):

        myEvent = problem.getEvent()
        g = problem.getEvent().getFunction()
        experiment = ot.MonteCarloExperiment()
        myMC = ot.ProbabilitySimulationAlgorithm(myEvent, experiment)
        myMC.setMaximumOuterSampling(maximumOuterSampling)
        myMC.setBlockSize(blockSize)
        myMC.setMaximumCoefficientOfVariation(coefficientOfVariation)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        myMC.run()
        resultMC = myMC.getResult()
        level = 0.95
        c95 = resultMC.getConfidenceLength(level)
        probabilityEstime = resultMC.getProbabilityEstimate()
        pmin = probabilityEstime - 0.5 * c95
        pmax = probabilityEstime + 0.5 * c95
        numberOfFunctionEvaluationsMonteCarlo = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        probabilityEstime = resultMC.getProbabilityEstimate()
        absolueError = abs(probabilityEstime - problem.getProbability())
        numberOfCorrectDigits = computeLogRelativeError(
            problem.getProbability(), probabilityEstime
        )
        return [
            probabilityEstime,
            absolueError,
            numberOfCorrectDigits,
            numberOfFunctionEvaluationsMonteCarlo,
            pmin,
            pmax,
        ]

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

        if nearestPointAlgo == "AbdoRackwitz":
            solver = ot.AbdoRackwitz()
        elif nearestPointAlgo == "Cobyla":
            solver = ot.Cobyla()
        elif nearestPointAlgo == "SQP":
            solver = ot.SQP()
        else:
            raise NameError(
                "Nearest point algorithm name must be \
                            'AbdoRackwitz', 'Cobyla' or 'SQP'."
            )

        solver.setMaximumEvaluationNumber(maximumEvaluationNumber)
        solver.setMaximumAbsoluteError(maximumAbsoluteError)
        solver.setMaximumRelativeError(maximumRelativeError)
        solver.setMaximumResidualError(maximumResidualError)
        solver.setMaximumConstraintError(maximumConstraintError)

        myEvent = problem.getEvent()
        inputVector = myEvent.getAntecedent()
        myDistribution = inputVector.getDistribution()
        g = problem.getEvent().getFunction()
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algoFORM = ot.FORM(solver, myEvent, myDistribution.getMean())
        algoFORM.run()
        resultFORM = algoFORM.getResult()
        standardSpaceDesignPoint = resultFORM.getStandardSpaceDesignPoint()
        d = myDistribution.getDimension()
        myImportance = ot.Normal(
            standardSpaceDesignPoint, [1.0] * d, ot.CorrelationMatrix(d)
        )

        experiment = ot.ImportanceSamplingExperiment(myImportance)
        algo = ot.ProbabilitySimulationAlgorithm(ot.StandardEvent(myEvent), experiment)
        algo.setMaximumCoefficientOfVariation(coefficientOfVariation)
        algo.setMaximumOuterSampling(maximumOuterSampling)
        algo.setConvergenceStrategy(ot.Full())
        algo.run()
        resultTirage = algo.getResult()
        numberOfFunctionEvaluationsTirage = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        probabilityEstime = resultTirage.getProbabilityEstimate()
        level = 0.95
        c95 = resultTirage.getConfidenceLength(level)
        pmin = probabilityEstime - 0.5 * c95
        pmax = probabilityEstime + 0.5 * c95
        absolueError = abs(probabilityEstime - problem.getProbability())
        numberOfCorrectDigits = computeLogRelativeError(
            problem.getProbability(), probabilityEstime
        )

        return [
            probabilityEstime,
            absolueError,
            numberOfCorrectDigits,
            numberOfFunctionEvaluationsTirage,
            pmin,
            pmax,
        ]

    def SubsetSampling(
        problem, maximumOuterSampling=5000, coefficientOfVariation=0.1, blockSize=1
    ):
        myEvent = problem.getEvent()
        g = problem.getEvent().getFunction()
        mySS = ot.SubsetSampling(myEvent)
        mySS.setMaximumOuterSampling(maximumOuterSampling)

        mySS.setMaximumCoefficientOfVariation(coefficientOfVariation)
        mySS.setBlockSize(blockSize)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        mySS.run()
        numberOfFunctionSS = g.getEvaluationCallsNumber() - initialNumberOfCall
        resultSS = mySS.getResult()
        probabilityEstime = resultSS.getProbabilityEstimate()
        level = 0.95
        c95 = resultSS.getConfidenceLength(level)
        pmin = probabilityEstime - 0.5 * c95
        pmax = probabilityEstime + 0.5 * c95
        absolueError = abs(probabilityEstime - problem.getProbability())
        numberOfCorrectDigits = computeLogRelativeError(
            problem.getProbability(), probabilityEstime
        )

        return [
            probabilityEstime,
            absolueError,
            numberOfCorrectDigits,
            numberOfFunctionSS,
            pmin,
            pmax,
        ]
