#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""
Class to define a sensitivity benchmark problem.
"""

class SensitivityBenchmarkProblem:
    def __init__(self, name, distribution, function, \
                 firstOrderIndices, totalOrderIndices):
        """
        Creates a reliability problem.
        
        Parameters
        ----------
        thresholdEvent : ot.ThresholdEvent
            The event.

        distribution : ot.Distribution
            The input distribution.
            
        function : ot.Function
            The model.

        firstOrderIndices : ot.Point
            The first order indices.
            
        totalOrderIndices : ot.Point
            The total order indices.
                
        Example
        -------
        problem  = ReliabilityBenchmarkProblem(thresholdEvent)
        """
        self.name = name
        self.distribution = distribution
        self.function = function
        self.firstOrderIndices = firstOrderIndices
        self.totalOrderIndices = totalOrderIndices
        return None

    def getInputDistribution(self):
        return self.distribution
    
    def getFunction(self):
        return self.function

    def getName(self):
        return self.name

    def getFirstOrderIndices(self):
        return self.firstOrderIndices
    
    def getTotalOrderIndices(self):
        return self.totalOrderIndices