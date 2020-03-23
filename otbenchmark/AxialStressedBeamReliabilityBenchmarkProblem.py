#!/usr/bin/python
# coding:utf-8
"""
Class to define a axial stressed beam benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot

class AxialStressedBeamReliabilityBenchmarkProblem(ReliabilityBenchmarkProblem):
    def __init__(self):
        """
        Creates a axial stressed beam reliability problem.
        
        Parameters
        none
        
        Description
        Creates a axial stressed beam reliability problem.
        
        Example
        problem  = AxialStressedBeamReliabilityBenchmarkProblem()
        """
        limitStateFunction = ot.SymbolicFunction(['R', 'F'], ['R-F/(pi_*100.0)'])
        
        R_dist = ot.LogNormalMuSigma(300.0, 30.0, 0.0).getDistribution()
        R_dist.setName('Yield strength')
        R_dist.setDescription('R')
        
        F_dist = ot.Normal(75000., 5000.)
        F_dist.setName('Traction_load')
        F_dist.setDescription('F')
        
        myDistribution = ot.ComposedDistribution([R_dist, F_dist])
        
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(limitStateFunction, inputRandomVector)
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), 0.0)

        name = "Axial stressed beam"
        probability = 0.02920
        super(AxialStressedBeamReliabilityBenchmarkProblem, self).__init__(name, thresholdEvent, probability)
        
        return None
