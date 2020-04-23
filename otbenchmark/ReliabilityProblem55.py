# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 10:22:51 2020

@author: Jebroun
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot
import numpy as np

class ReliabilityProblem55(ReliabilityBenchmarkProblem):
    def __init__(self, threshold = 0.0, 
                 a1 = -1.0,
                 b1 = 1.0,
                 a2 = -1.0,
                 b2 = 1.0):
        """
        Creates a reliability problem RP55.

        The event is {g(X) < threshold} where 
        
        g(x1, x2) = 
        
        We have x1 ~ Uniform(a1, b1) and x2 ~ Uniform(a2, b2). 
        
        Parameters
        ----------
        threshold : float
            The threshold. 
        
        a1 , b1  : float
            Parameters of the X1 uniform distribution. 
        
        
        a2 , b2 : float
            Parameters of the X2 uniform distribution. 
        """
        def f(x):
             g1 = 0.2 + 0.6 * (x[0] - x[1]) ** 4 - (x[0] - x[1]) / np.sqrt(2)
             g2 = 0.2 + 0.6 * (x[0] - x[1]) ** 4 + (x[ 0] - x[ 1]) / np.sqrt(2)
             g3 = (x[0] - x[1]) + 5 / np.sqrt(2) - 2.2
             g4 = (x[1] - x[0]) + 5 / np.sqrt(2) - 2.2
             g = np.min([g1, g2, g3, g4])
    
             y = [g]
             return y
            
   
        limitStateFunction = ot.PythonFunction(2, 1, f)                                        
                                                 
        X1 = ot.Uniform(a1, b1)
        X1.setDescription(["X1"])
        X2 = ot.Uniform(a2, b2)
        X2.setDescription(["X2"])

        myDistribution = ot.ComposedDistribution([X1, X2])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(limitStateFunction, inputRandomVector)
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(),
                                           threshold)

        name = "RP55"
        probability = 0.36
        super(ReliabilityProblem55, self).__init__(name, thresholdEvent, probability)
        
        return None