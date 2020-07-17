# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 08:35:15 2020

@author: Jebroun
"""

import openturns as ot


class SubsetFactory(ot.SubsetSampling):
    def __init__(self, problem):
        myEvent = problem.getEvent()
        super(SubsetFactory, self).__init__(myEvent)
        return None
