#!/usr/bin/python
# coding:utf-8
"""
Class to define a benchmark problem.
"""

class ReliabilityBenchmarkProblem:
    def __init__(self, name, thresholdEvent, probability, description = ""):
        """
        Creates a reliability problem.
        
        Parameters
        thresholdEvent : a ThresholdEvent, the event
        
        Description
        Creates a reliability problem.
        
        Example
        problem  = ReliabilityBenchmarkProblem(name, thresholdEvent, probability)
        """
        self.name = name
        self.thresholdEvent = thresholdEvent
        self.probability = probability

        return None

    def getEvent(self):
        return self.thresholdEvent
    
    def getProbability(self):
        return self.probability

    def getName(self):
        return self.name
