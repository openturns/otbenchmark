# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:28:04 2020

@author: Jebroun
"""

import openturns as ot


class SORMFactory(ot.SORM):
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
        Creates a SORM algorithm.

        We create a SORM algorithm based on the problem event and the AbdoRackwitz
        optimization solver.

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
        super(SORMFactory, self).__init__(solver, myEvent, physicalStartingPoint)
        return None
