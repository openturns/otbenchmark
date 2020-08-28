# -*- coding: utf-8 -*-
"""
Create a LHS object.
"""

import openturns as ot


class LHS(ot.LHS):
    def __init__(self, problem):
        """
        Creates a LHS algorithm.

        Parameters
        ----------
        problem : ot.ReliabilityBenchmarkProblem
            The problem.
        """
        event = problem.getEvent()
        super(LHS, self).__init__(event)
        return None
