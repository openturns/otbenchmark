#!/usr/bin/python
# coding:utf-8
"""
Class to define the R-S benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot

class RminusSReliabilityBenchmarkProblem(ReliabilityBenchmarkProblem):
    def __init__(self, threshold = 0.0):
        """
        Creates a R-S reliability problem.
        The event is {R - S < threshold}.
        
        Parameters
        ----------
        threshold : float
            The threshold. 
                
        Example
        -------
        problem  = RminusSReliabilityBenchmarkProblem()
        """
        limitStateFunction = ot.SymbolicFunction(["R", "S"],["R - S"])
        
        R = ot.Normal(4., 1.)
        R.setDescription("R")
        
        S = ot.Normal(2., 1.)
        S.setDescription("S")
        
        myDistribution = ot.ComposedDistribution([R, S])
        
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(limitStateFunction, inputRandomVector)
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "R-S"
        diff = R - S
        probability = diff.computeCDF(threshold)
        super(RminusSReliabilityBenchmarkProblem, self).__init__(name, thresholdEvent, probability)
        
        return None
