# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 11:37:47 2020

@author: Jebroun
"""
import openturns as ot
import otbenchmark as otb

"""
Static methods to create a liste of all reliability problems.
"""


class mini_Benchmark:
    def problemsliste():
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
        Liste_problem = [
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
        ]
        return Liste_problem

    def FORM(Problem):
        # Cobyla algorithm
        myCobyla = ot.Cobyla()
        # Resolution options:
        eps = 1e-3
        myCobyla.setMaximumEvaluationNumber(100)
        myCobyla.setMaximumAbsoluteError(eps)
        myCobyla.setMaximumRelativeError(eps)
        myCobyla.setMaximumResidualError(eps)
        myCobyla.setMaximumConstraintError(eps)
        myEvent = Problem.getEvent()
        inputVector = myEvent.getAntecedent()
        myDistribution = inputVector.getDistribution()
        g = Problem.getEvent().getFunction()
        algoFORM = ot.FORM(myCobyla, myEvent, myDistribution.getMean())
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algoFORM.run()
        resultFORM = algoFORM.getResult()
        numberOfFunctionEvaluationsFORM = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        return [resultFORM, numberOfFunctionEvaluationsFORM]

    def SORM(Problem):
        # Cobyla algorithm
        myCobyla = ot.Cobyla()
        # Resolution options:
        eps = 1e-3
        myCobyla.setMaximumEvaluationNumber(100)
        myCobyla.setMaximumAbsoluteError(eps)
        myCobyla.setMaximumRelativeError(eps)
        myCobyla.setMaximumResidualError(eps)
        myCobyla.setMaximumConstraintError(eps)
        myEvent = Problem.getEvent()
        inputVector = myEvent.getAntecedent()
        myDistribution = inputVector.getDistribution()
        g = Problem.getEvent().getFunction()
        algoSORM = ot.SORM(myCobyla, myEvent, myDistribution.getMean())
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algoSORM.run()
        resultSORM = algoSORM.getResult()
        numberOfFunctionEvaluationsSORM = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        return [resultSORM, numberOfFunctionEvaluationsSORM]

    def MonteCarloSampling(Problem, NBS, cv):

        myEvent = Problem.getEvent()
        g = Problem.getEvent().getFunction()
        experiment = ot.MonteCarloExperiment()
        myMC = ot.ProbabilitySimulationAlgorithm(myEvent, experiment)
        myMC.setMaximumOuterSampling(NBS)
        myMC.setBlockSize(1)
        myMC.setMaximumCoefficientOfVariation(cv)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        myMC.run()
        resultMC = myMC.getResult()
        numberOfFunctionEvaluationsMonteCarlo = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        return [
            resultMC,
            numberOfFunctionEvaluationsMonteCarlo,
            myMC.drawProbabilityConvergence(),
        ]

    def ImportanceSampling(Problem):
        # Cobyla algorithm
        myCobyla = ot.Cobyla()
        # Resolution options:
        eps = 1e-3
        myCobyla.setMaximumEvaluationNumber(100)
        myCobyla.setMaximumAbsoluteError(eps)
        myCobyla.setMaximumRelativeError(eps)
        myCobyla.setMaximumResidualError(eps)
        myCobyla.setMaximumConstraintError(eps)

        myEvent = Problem.getEvent()
        inputVector = myEvent.getAntecedent()
        myDistribution = inputVector.getDistribution()
        g = Problem.getEvent().getFunction()
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algoFORM = ot.FORM(myCobyla, myEvent, myDistribution.getMean())
        algoFORM.run()
        resultFORM = algoFORM.getResult()
        standardSpaceDesignPoint = resultFORM.getStandardSpaceDesignPoint()
        d = myDistribution.getDimension()
        myImportance = ot.Normal(
            standardSpaceDesignPoint, [1.0] * d, ot.CorrelationMatrix(d)
        )

        experiment = ot.ImportanceSamplingExperiment(myImportance)
        algo = ot.ProbabilitySimulationAlgorithm(ot.StandardEvent(myEvent), experiment)
        algo.setMaximumCoefficientOfVariation(0.1)
        algo.setMaximumOuterSampling(50000)
        algo.setConvergenceStrategy(ot.Full())
        algo.run()
        resultTirage = algo.getResult()
        graph = algo.drawProbabilityConvergence()
        numberOfFunctionEvaluationsTirage = (
            g.getEvaluationCallsNumber() - initialNumberOfCall
        )
        return [resultTirage, numberOfFunctionEvaluationsTirage, graph]

    def SubsetSampling(Problem):
        myEvent = Problem.getEvent()
        g = Problem.getEvent().getFunction()
        mySS = ot.SubsetSampling(myEvent)
        mySS.setMaximumOuterSampling(5000)
        mySS.setMaximumCoefficientOfVariation(0.1)
        mySS.setBlockSize(1)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        mySS.run()
        graph = mySS.drawProbabilityConvergence()
        resultSS = mySS.getResult()
        numberOfFunctionSS = g.getEvaluationCallsNumber() - initialNumberOfCall
        return [resultSS, numberOfFunctionSS, graph]
