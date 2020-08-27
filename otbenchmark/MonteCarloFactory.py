# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:45:25 2020

@author: Jebroun
"""

import openturns as ot


class MonteCarloFactory(ot.ProbabilitySimulationAlgorithm):
    def __init__(self, problem):
        """
        Creates a Monte-Carlo algorithm.

        We create a MonteCarloExperiment and we create
        a ProbabilitySimulationAlgorithm based on the problem event.

        Parameters
        ----------
        problem : ot.ReliabilityBenchmarkProblem
            The problem.
        """
        myEvent = problem.getEvent()
        experiment = ot.MonteCarloExperiment()
        super(MonteCarloFactory, self).__init__(myEvent, experiment)
        return None
