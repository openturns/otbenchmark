# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:18:59 2020

@author: Jebroun
"""

"""
Class to define the ReliabilityProblem25 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot
import numpy as np

class ReliabilityProblem25(ReliabilityBenchmarkProblem):
    def __init__(self, threshold = 0.0, 
                 mu1 = 0.0,
                 sigma1 = 1.0,
                 mu2 = 0.0,
                 sigma2 = 1.0):
        """
        Creates a reliability problem RP25.

        The event is {g(X) < threshold} where 
        
        g(x1, x2) = max(x1^2 -8 * x2 + 16, -16 * x1 + x2 + 32)
        
        We have x1 ~ Normal(mu1, sigma1) and x2 ~ Normal(mu2, sigma2). 
        
        Parameters
        ----------
        threshold : float
            The threshold. 
        
        mu1 : float
            The mean of the X1 gaussian distribution. 
        
        sigma1 : float
            The standard deviation of the X1 gaussian distribution. 
        
        mu2 : float
            The mean of the X2 gaussian distribution. 
        
        sigma2 : float
            The standard deviation of the X2 gaussian distribution. 
        """
        limitStateFunction = ot.SymbolicFunction(["x1", "x2"], [" max(x1^2 -8*x2 +16 , -16*x1 +x2 +32 ) "])
        X1 = ot.Normal(mu1, sigma1)
        X1.setDescription(["X1"])
        X2 = ot.Normal(mu2, sigma2)
        X2.setDescription(["X2"])

        myDistribution = ot.ComposedDistribution([X1, X2])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(limitStateFunction, inputRandomVector)
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(),
                                           threshold)

        name = "RP25"
        
        probability = 0.00000614
        super(ReliabilityProblem25, self).__init__(name, thresholdEvent, probability)
        
        return None

