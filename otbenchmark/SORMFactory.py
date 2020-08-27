# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:28:04 2020

@author: Jebroun
"""

import openturns as ot


class SORMFactory(ot.SORM):
    def __init__(self, problem):
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
        solver = ot.AbdoRackwitz()
        physicalStartingPoint = myDistribution.getMean()
        super(SORMFactory, self).__init__(solver, myEvent, physicalStartingPoint)
        return None
