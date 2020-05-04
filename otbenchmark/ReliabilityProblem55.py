# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 10:22:51 2020

@author: Jebroun
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem55(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, a1=-1.0, b1=1.0, a2=-1.0, b2=1.0):
        """
        Creates a reliability problem RP55.

        The event is {g(X) < threshold} where
        We have x1 ~ Uniform(a1, b1) and x2 ~ Uniform(a2, b2).
        ***
        Parameters
        ----------
        threshold : float
            The threshold.
        a1 , b1  : float
            Parameters of the X1 uniform distribution.
        a2 , b2 : float
            Parameters of the X2 uniform distribution.
        """
        equations = ["var g1 := 0.2 + 0.6 * (x0 - x1)^4 - (x0 - x1) / sqrt(2)"]
        equations.append("var g2 := 0.2 + 0.6 * (x0 - x1)^4 + (x0 - x1) / sqrt(2)")
        equations.append("var g3 := (x0 - x1) + 5 / sqrt(2) - 2.2")
        equations.append("var g4 := (x1 - x0) + 5 / sqrt(2) - 2.2")
        equations.append("gsys := min(g1, g2, g3, g4)")
        formula = ";".join(equations)
        limitStateFunction = ot.SymbolicFunction(["x0", "x1"], ["gsys"], formula)
        print(formula)
        X1 = ot.Uniform(a1, b1)
        X1.setDescription(["X1"])
        X2 = ot.Uniform(a2, b2)
        X2.setDescription(["X2"])

        myDistribution = ot.ComposedDistribution([X1, X2])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP55"
        probability = 0.36
        super(ReliabilityProblem55, self).__init__(name, thresholdEvent, probability)
        return None
