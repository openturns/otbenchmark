#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""
Class to define a benchmark problem.
"""

import openturns as ot

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
        """
        Returns the event.
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        event: ot.ThresholdEvent
            The event.
        """
        return self.thresholdEvent
    
    def getProbability(self):
        """
        Returns the probability.
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        probability: float
            The probability of the event.
        """
        return self.probability

    def getName(self):
        """
        Returns the name of the problem.
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        name: str
            The name of the problem.
        """
        return self.name
    
    def computeBeta(self):
        """
        Returns the beta of the reliability problem. 
        This is the quantile of the 
        probability of a standard gaussian distribution. 
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        beta: float
            The beta of the problem.
        """
        beta = ot.Normal().computeQuantile(self.probability, True)[0]
        return beta
    
    def __str__(self):
        g = self.thresholdEvent.getFunction()
        beta = ot.Normal().computeQuantile(self.probability, True)[0]
        threshold = self.thresholdEvent.getThreshold()
        inputVector = self.thresholdEvent.getAntecedent()
        distribution = inputVector.getDistribution()
        s = "Name: %s \nFunction: %s\nProbability= %s\nThreshold= %s\nDistribution=%s" % (
            self.name, g, self.probability, threshold, distribution)
        return s
    