# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:37:41 2020

@author: Jebroun
"""

import openturns as ot


class FORMISFactory(ot.ProbabilitySimulationAlgorithm):
    def __init__(
        self,
        problem,
        nearestPointAlgo="AbdoRackwitz",
        maximumEvaluationNumber=100,
        maximumAbsoluteError=1.0e-3,
        maximumRelativeError=1.0e-3,
        maximumResidualError=1.0e-3,
        maximumConstraintError=1.0e-3,
    ):
        """
        Creates a FORM-IS algorithm.

        We first create a FORM object based on the AbdoRackwitz
        and run it to get the design point in the standard space.
        Then we create an ImportanceSamplingExperiment based on the gaussian
        distribution, centered on the design point.
        Finally, we create a ProbabilitySimulationAlgorithm.

        Parameters
        ----------
        problem : ot.ReliabilityBenchmarkProblem
            The problem.
        """
        myEvent = problem.getEvent()
        inputVector = myEvent.getAntecedent()
        myDistribution = inputVector.getDistribution()
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
        physicalStartingPoint = myDistribution.getMean()
        algoFORM = ot.FORM(solver, myEvent, physicalStartingPoint)
        algoFORM.run()
        resultFORM = algoFORM.getResult()
        standardSpaceDesignPoint = resultFORM.getStandardSpaceDesignPoint()
        d = myDistribution.getDimension()
        myImportance = ot.Normal(d)
        myImportance.setMean(standardSpaceDesignPoint)
        experiment = ot.ImportanceSamplingExperiment(myImportance)
        standardEvent = ot.StandardEvent(myEvent)
        super(FORMISFactory, self).__init__(standardEvent, experiment)
        return None
