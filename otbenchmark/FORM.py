# -*- coding: utf-8 -*-
"""
Create a FORM object.
"""

import openturns as ot


class FORM(ot.FORM):
    def __init__(self, problem, nearestPointAlgorithm):
        """
        Creates a FORM algorithm.

        We create a FORM algorithm based on the problem event and the AbdoRackwitz
        optimization solver.

        Parameters
        ----------
        problem : ot.ReliabilityBenchmarkProblem
            The problem.
        nearestPointAlgorithm : ot.OptimizationAlgorithm
            Optimization algorithm used to search the design point.
        """
        myEvent = problem.getEvent()
        inputVector = myEvent.getAntecedent()
        myDistribution = inputVector.getDistribution()
        physicalStartingPoint = myDistribution.getMean()
        super(FORM, self).__init__(
            nearestPointAlgorithm, myEvent, physicalStartingPoint
        )
        return None
