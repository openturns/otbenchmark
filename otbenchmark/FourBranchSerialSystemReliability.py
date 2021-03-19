#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define the four-branch serial system from Waarts."""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class FourBranchSerialSystemReliability(ReliabilityBenchmarkProblem):
    def __init__(self):
        """
        Creates the four-branch serial system from Waarts.

        References
        ----------

        Waarts, P.-H. (2000). Structural reliability using finite element
        methods: an appraisal of DARS: Directional Adaptive Response Surface
        Sampling. Ph. D. thesis, Technical University of Delft, The
        Netherlands. Pages 58, 69, 160.

        Thèse Vincent Dubourg 2011, Méta-modèles adaptatifs pour l’analyse
        de fiabilité et l’optimisation sous contrainte fiabiliste,
        section "A two-dimensional four-branch serial system", page 182

        Parameters
        ----------
        None.

        Example
        -------
        problem  = FourBranchSerialSystemReliability()
        """
        formulaList = [
            "var y0 := 3 + 0.1 * (x0 - x1)^2 - (x0 + x1) / sqrt(2)",
            "var y1 := 3 + 0.1 * (x0 - x1)^2 + (x0 + x1) / sqrt(2)",
            "var y2 := x0 - x1 + 7 / sqrt(2)",
            "var y3 := x1 - x0 + 7 / sqrt(2)",
            "y := min(y0,y1,y2,y3)",
        ]
        formula = ";".join(formulaList)
        limitStateFunction = ot.SymbolicFunction(["x0", "x1"], ["y"], formula)

        x0 = ot.Normal(0.0, 1.0)
        x1 = ot.Normal(0.0, 1.0)
        inputDistribution = ot.ComposedDistribution((x0, x1))
        inputRandomVector = ot.RandomVector(inputDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), 0.0)

        name = "Four-branch serial system"
        beta = 2.85
        probability = ot.Normal().computeComplementaryCDF(beta)
        super(FourBranchSerialSystemReliability, self).__init__(
            name, thresholdEvent, probability
        )

        return None
