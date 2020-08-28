# -*- coding: utf-8 -*-
"""
Create a SORM object.
"""

import openturns as ot


class SORM(ot.SORM):
    def __init__(self, problem, nearestPointAlgorithm):
        """
        Creates a SORM algorithm.

        We create a SORM algorithm based on the problem event and the AbdoRackwitz
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
        super(SORM, self).__init__(
            nearestPointAlgorithm, myEvent, physicalStartingPoint
        )
        return None
