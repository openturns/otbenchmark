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


class mini_Benchmark:
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
        AbsolueError = abs(probabilityEstime - problem.getProbability())
        NumberCorrectDigits = computeLogRelativeError(
            problem.getProbability(), probabilityEstime
        )

        return [
            probabilityEstime,
            AbsolueError,
            NumberCorrectDigits,
            numberOfFunctionEvaluationsFORM,
        ]

    def printResultFORM(ResultForm):
        s = (
            "The estimated probability  with FORM = %s \n "
            "The Absolue error = %s\n "
            "Number of correct digits = %s\n "
            "number of function evaluations with FORM = %s"
        ) % (ResultForm[0], ResultForm[1], ResultForm[2], ResultForm[3],)
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
        AbsolueError = abs(probabilityEstime - problem.getProbability())
        NumberCorrectDigits = computeLogRelativeError(
            problem.getProbability(), probabilityEstime
        )
        return [
            probabilityEstime,
            AbsolueError,
            NumberCorrectDigits,
            numberOfFunctionEvaluationsSORM,
        ]

    def printResultSORM(ResultSorm):
        s = (
            "The estimated probability  with SORM = %s \n"
            "The Absolue error = %s\n "
            "Number of correct digits = %s\n "
            "number of function evaluations with SORM = %s"
        ) % (ResultSorm[0], ResultSorm[1], ResultSorm[2], ResultSorm[3],)
        return s

    def MonteCarloSampling(
        problem, maximumOuterSampling=1000, coefficientOfVariation=0.1, BlockSize=1
    ):

        myEvent = problem.getEvent()
        g = problem.getEvent().getFunction()
        experiment = ot.MonteCarloExperiment()
        myMC = ot.ProbabilitySimulationAlgorithm(myEvent, experiment)
        myMC.setMaximumOuterSampling(maximumOuterSampling)
        myMC.setBlockSize(BlockSize)
        myMC.setMaximumCoefficientOfVariation(coefficientOfVariation)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        myMC.run()
        resultMC = myMC.getResult()
        numberOfFunctionEvaluationsMonteCarlo = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        graph = myMC.drawProbabilityConvergence()
        probabilityEstime = resultMC.getProbabilityEstimate()
        AbsolueError = abs(probabilityEstime - problem.getProbability())
        NumberCorrectDigits = computeLogRelativeError(
            problem.getProbability(), probabilityEstime
        )
        return [
            probabilityEstime,
            AbsolueError,
            NumberCorrectDigits,
            numberOfFunctionEvaluationsMonteCarlo,
            graph,
        ]

    def printResultMC(ResultMC):
        s = (
            "The estimated probability  with Monte Carlo = %s \n "
            "The Absolue error = %s\n "
            "Number of correct digits = %s\n "
            "number of function evaluations with Monte Carlo = %s"
        ) % (ResultMC[0], ResultMC[1], ResultMC[2], ResultMC[3],)
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

        graph = algo.drawProbabilityConvergence()
        numberOfFunctionEvaluationsTirage = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        probabilityEstime = resultTirage.getProbabilityEstimate()
        AbsolueError = abs(probabilityEstime - problem.getProbability())
        NumberCorrectDigits = computeLogRelativeError(
            problem.getProbability(), probabilityEstime
        )

        return [
            probabilityEstime,
            AbsolueError,
            NumberCorrectDigits,
            numberOfFunctionEvaluationsTirage,
            graph,
        ]

    def printResultFORMIS(ResultIS):
        s = (
            "The estimated probability  with Importance Sampling = %s \n "
            "The Absolue error = %s\n "
            "Number of correct digits = %s\n "
            "number of function evaluations with Importance Sampling = %s"
        ) % (ResultIS[0], ResultIS[1], ResultIS[2], ResultIS[3],)
        return s

    def SubsetSampling(
        problem, maximumOuterSampling=5000, coefficientOfVariation=0.1, BlockSize=1
    ):
        myEvent = problem.getEvent()
        g = problem.getEvent().getFunction()
        mySS = ot.SubsetSampling(myEvent)
        mySS.setMaximumOuterSampling(maximumOuterSampling)

        mySS.setMaximumCoefficientOfVariation(coefficientOfVariation)
        mySS.setBlockSize(BlockSize)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        mySS.run()
        graph = mySS.drawProbabilityConvergence()
        resultSS = mySS.getResult()
        probabilityEstime = resultSS.getProbabilityEstimate()
        AbsolueError = abs(probabilityEstime - problem.getProbability())
        NumberCorrectDigits = computeLogRelativeError(
            problem.getProbability(), probabilityEstime
        )
        numberOfFunctionSS = g.getEvaluationCallsNumber() - initialNumberOfCall
        return [
            probabilityEstime,
            AbsolueError,
            NumberCorrectDigits,
            numberOfFunctionSS,
            graph,
        ]

    def printResultSubset(ResultSS):
        s = (
            "The estimated probability  with Subset Sampling = %s \n "
            "The Absolue error = %s\n "
            "Number of correct digits = %s\n "
            "number of function evaluations with Subset Sampling = %s"
        ) % (ResultSS[0], ResultSS[1], ResultSS[2], ResultSS[3],)
        return s
