#!/usr/bin/python
# coding:utf-8
# Copyright 2021 EDF
"""Class to define a Borgonovo sensitivity benchmark problem."""

from otbenchmark.SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot


class BorgonovoSensitivity(SensitivityBenchmarkProblem):
    """Class to define a Borgonovo sensitivity benchmark problem."""

    def __init__(self):
        """
        Create a Borgonovo sensitivity problem.

        The function is defined by the equation:

        .. math::
            g(x) = x1 * x2 + x3

        where x1, x2, x3 ~ U(0, 1).

        The input random variables are independent.

        Examples
        --------
        >>> import otbenchmark as otb
        >>> problem = otb.BorgonovoSensitivity()

        Notes
        -----
        The dimension and parameters of this problem cannot be changed.
        The Sobol' sensitivity indices are exact.

        The model was first introduced in (Borgonovo, 2017).

        References
        ----------
        * Borgonovo, Emanuele. "Sensitivity analysis."
          An Introduction for the Management Scientist.
          International Series in Operations Research and Management Science.
          Cham, Switzerland: Springer (2017).
          p.18 and p.157.
        """

        dimension = 3
        function = ot.SymbolicFunction(["x1", "x2", "x3"], ["x1 * x2 + x3"])
        function.setOutputDescription(["Y"])

        # Define the distribution
        distributionList = [ot.Uniform(0.0, 1.0)] * dimension
        distribution = ot.ComposedDistribution(distributionList)

        name = "Borgonovo"

        # Compute exact indices
        firstOrderIndices = ot.Point([3.0 / 19.0, 3.0 / 19.0, 12.0 / 19.0])
        totalOrderIndices = ot.Point([4.0 / 19.0, 4.0 / 19.0, 12.0 / 19.0])

        super(BorgonovoSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None
