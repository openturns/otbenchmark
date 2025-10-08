#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define the four-branch serial system from Waarts."""

from ._ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class FourBranchSerialSystemReliability(ReliabilityBenchmarkProblem):
    def __init__(self):
        r"""
        Creates the four-branch serial system from Waarts.
        The event is :math:`\{g(\boldsymbol{X}) < \text{threshold}\}` where:

        .. math::

            g(X_1, X_2) = \min(Y_1, Y_2, Y_3, Y_4)

        with:

        .. math::

            Y_1 &= 3 + 0.1 (X_1 - X_2)^2 - \frac{X_1 + X_2}{\sqrt{2}} \\
            Y_2 &= 3 + 0.1 (X_1 - X_2)^2 + \frac{X_1 + X_2}{\sqrt{2}} \\
            Y_3 &= X_1 - X_2 + \frac{7}{\sqrt{2}} \\
            Y_4 &= X_2 - X_1 + \frac{7}{\sqrt{2}}

        We have:

        * :math:`X_1 \sim \mathcal{N}(\mu_1, \sigma_1)` and
        * :math:`X_2 \sim \mathcal{N}(\mu_2, \sigma_2)`.

        References
        ----------

        - Waarts, P.-H. (2000). Structural reliability using finite element
          methods: an appraisal of DARS: Directional Adaptive Response Surface
          Sampling. Ph. D. thesis, Technical University of Delft, The
          Netherlands. Pages 58, 69, 160.

        - Thèse Vincent Dubourg 2011, Méta-modèles adaptatifs pour l’analyse
          de fiabilité et l’optimisation sous contrainte fiabiliste,
          section "A two-dimensional four-branch serial system", page 182

        Examples
        --------
        >>> import otbenchmark as otb
        >>> problem = otb.FourBranchSerialSystemReliability()
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
        probability = 0.2222795066194439887212863444e-2
        super(FourBranchSerialSystemReliability, self).__init__(
            name, thresholdEvent, probability
        )

        return None
