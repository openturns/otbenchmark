#!/usr/bin/python
# coding:utf-8
"""
Class to define a sensitivity benchmark problem.
"""

class SensitivityBenchmarkProblem:
    def __init__(self, name, distribution, function, \
                 firstOrderIndices, totalOrderIndices):
        """
        Creates a reliability problem.
        
        Parameters
        thresholdEvent : a ThresholdEvent, the event
        distribution : a Distribution, the input distribution
        function : a Function, the model
        firstOrderIndices : a Point, the first order indices
        totalOrderIndices : a Point, the total order indices
        
        Description
        Creates a reliability problem.
        
        Example
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