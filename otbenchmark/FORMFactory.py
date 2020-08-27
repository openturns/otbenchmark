# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:39:10 2020

@author: Jebroun
"""

import openturns as ot


class FORMFactory(ot.FORM):
    def __init__(self, problem):
        """
        Creates a FORM algorithm.

        We create a FORM algorithm based on the problem event and the AbdoRackwitz
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
        super(FORMFactory, self).__init__(solver, myEvent, physicalStartingPoint)
        return None
