# -*- coding: utf-8 -*-
"""
A class to create a Subset algorithm.
"""

import openturns as ot


class SubsetSampling(ot.SubsetSampling):
    def __init__(self, problem):
        """
        Creates a SubsetSampling algorithm.

        Parameters
        ----------
        problem : ot.ReliabilityBenchmarkProblem
            The problem.
        """
        event = problem.getEvent()
        super(SubsetSampling, self).__init__(event)
        return None
