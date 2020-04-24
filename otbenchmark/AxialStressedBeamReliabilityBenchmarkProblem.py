#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define a axial stressed beam benchmark problem."""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot
import numpy as np


class AxialStressedBeamReliabilityBenchmarkProblem(ReliabilityBenchmarkProblem):
    """Class to define a axial stressed beam benchmark problem."""

    def __init__(self, threshold=0.0):
        """
        Create a axial stressed beam reliability problem.

        Parameters
        ----------
        threshold : float
            The threshold.

        Example
        -------
        problem  = AxialStressedBeamReliabilityBenchmarkProblem()
        """
        limitStateFunction = ot.SymbolicFunction(["R", "F"], ["R - F/(pi_ * 100.0)"])

        R_dist = ot.LogNormalMuSigma(300.0, 30.0, 0.0).getDistribution()
        R_dist.setName("Yield strength")
        R_dist.setDescription("R")

        F_dist = ot.Normal(75000.0, 5000.0)
        F_dist.setName("Traction_load")
        F_dist.setDescription("F")

        myDistribution = ot.ComposedDistribution([R_dist, F_dist])

        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), 0.0)

        name = "Axial stressed beam"
        diff = R_dist - F_dist / (np.pi * 100.0)
        probability = diff.computeCDF(threshold)
        super(AxialStressedBeamReliabilityBenchmarkProblem, self).__init__(
            name, thresholdEvent, probability
        )

        return None
