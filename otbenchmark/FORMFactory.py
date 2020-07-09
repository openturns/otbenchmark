# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:39:10 2020

@author: Jebroun
"""

import openturns as ot


class FORMFactory(ot.FORM):
    def __init__(self, problem):
        myEvent = problem.getEvent()
        inputVector = myEvent.getAntecedent()
        myDistribution = inputVector.getDistribution()
        solver = ot.AbdoRackwitz()
        super(FORMFactory, self).__init__(solver, myEvent, myDistribution.getMean())
        return None
