# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:37:41 2020

@author: Jebroun
"""

import openturns as ot


class FORMISFactory(ot.ProbabilitySimulationAlgorithm):
    def __init__(self, problem):

        myEvent = problem.getEvent()
        inputVector = myEvent.getAntecedent()
        myDistribution = inputVector.getDistribution()
        solver = ot.AbdoRackwitz()
        algoFORM = ot.FORM(solver, myEvent, myDistribution.getMean())
        algoFORM.run()
        resultFORM = algoFORM.getResult()
        standardSpaceDesignPoint = resultFORM.getStandardSpaceDesignPoint()
        d = myDistribution.getDimension()
        myImportance = ot.Normal(
            standardSpaceDesignPoint, [1.0] * d, ot.CorrelationMatrix(d)
        )

        experiment = ot.ImportanceSamplingExperiment(myImportance)
        super(FORMISFactory, self).__init__(ot.StandardEvent(myEvent), experiment)
        return None
