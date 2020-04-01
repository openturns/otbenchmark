#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""
Class to define a benchmark problem.
"""

class ReliabilityBenchmarkProblem:
    def __init__(self, name, thresholdEvent, probability, description = ""):
        """
        Creates a reliability problem.
        
        Parameters
        ----------
        thresholdEvent : ot.ThresholdEvent
            The event.
        
        Example
        -------
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
