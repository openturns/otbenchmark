#!/usr/bin/python
# coding:utf-8
# Copyright 2020 - 2021 EDF
"""Class to define a Dirichlet sensitivity benchmark problem."""

from ._SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot
import numpy as np
import sys


class DirichletFunction(ot.OpenTURNSPythonFunction):
    """
    The non-monotonic function of Morris f: R^20 -> R

    References
    ----------
    * Jean-Marc Martinez. Benchmark based on analytical functions (2008).
    http://gdr-mascotnum.math.cnrs.fr/data2/benchmarks/jm.pdf.
    """

    def __init__(self, alpha=ot.Point([1.0 / 2.0, 1.0 / 3.0, 1.0 / 4.0])):
        """
        Create the Dirichlet function

        Parameters
        ----------
        alpha : ot.Point(p), optional
            The coefficients of the model.

        Returns
        -------
        None.

        """
        self.alpha = alpha
        self.dimension = alpha.getDimension()
        ot.OpenTURNSPythonFunction.__init__(self, self.dimension, 1)

    def _exec(self, x):
        y = 1.0
        for i in range(self.dimension):
            factor = 2.0 * (1 + i) + 1.0
            if abs(x[i]) < sys.float_info.epsilon:
                a = factor
            else:
                a = np.sin(factor * np.pi * x[i]) / np.sin(np.pi * x[i])
            b = (a - 1.0) / np.sqrt(2.0 * (1 + i))
            y *= 1.0 + self.alpha[i] * b
        return [y]


class DirichletSensitivity(SensitivityBenchmarkProblem):
    """Class to define a Dirichlet sensitivity benchmark problem."""

    @staticmethod
    def ComputeIndices(alpha):
        """
        Compute the exact Sobol' indices of the Dirichlet test case.

        Parameters
        ----------
        alpha: ot.Point(n)
            The vector of alpha parameters.

        Returns
        -------
        exact : dict
            The exact expectation, variance, first order Sobol' indices,
            total order Sobol' indices.

        """
        dimension = alpha.getDimension()
        # Vector of squared alpha
        sqr_alpha = [alpha[i] ** 2 for i in range(dimension)]
        # Compute the mean of the output
        mean_y = 1

        # Compute the variance of the output
        product = 1.0
        for i in range(dimension):
            product *= 1.0 + sqr_alpha[i]
        variance_y = product - 1.0

        # Compute Sobol' indices
        s = ot.Point(dimension)
        for i in range(dimension):
            s[i] = sqr_alpha[i] / variance_y
        t = ot.Point(dimension)
        leading = (1.0 + variance_y) / variance_y
        for i in range(dimension):
            t[i] = leading * sqr_alpha[i] / (1.0 + sqr_alpha[i])

        exact = {
            "expectation": mean_y,
            "variance": variance_y,
            "S": s,
            "T": t,
        }
        return exact

    def __init__(self, alpha=ot.Point([1.0 / 2.0, 1.0 / 3.0, 1.0 / 4.0])):
        """
        Create a Dirichlet sensitivity problem.

        The function is defined by the equation:

        .. math::
            g(x) = prod_{i=1}^p (1 + g_i(x[i]))

        where:

        .. math::
            g_i(x) = alpha_i * d_i(x)

        for any x in [0, 1], where d_i is the Dirichlet kernel:

        .. math::
            d_i(x) = (1 / sqrt(2i)) * (sin((2i + 1) pi x) / sin(pi x) - 1)

        for i=1, 2, ..., p.

        By continuity, we set:

        .. math::
            d_i(0) = 1 / sqrt(2i) for i=1, 2, ..., p.

        The Dirichlet kernel has the properties:

        .. math::
            int_0^1 d_i(x) dx = 0,
            int_0^1 d_i(x)^2 dx = 0.

        The input random variables are independent.

        Parameters
        ----------
        alpha : ot.Point(p)
            The vector of coefficients.

        Examples
        --------
        >>> import otbenchmark as otb
        >>> problem = otb.DirichletSensitivity()

        Notes
        -----

        The dimension of this problem can be changed, but
        its parameters can.
        The Sobol' sensitivity indices are computed from the values
        of the parameters.

        The model was first introduced in (Martinez, 2008).

        References
        ----------
        * Jean-Marc Martinez. Benchmark based on analytical functions (2008).
          http://gdr-mascotnum.math.cnrs.fr/data2/benchmarks/jm.pdf.

        """

        dimension = alpha.getDimension()
        function = ot.Function(DirichletFunction(alpha))

        # Define the distribution
        distributionList = [ot.Uniform(0.0, 1.0)] * dimension
        distribution = ot.ComposedDistribution(distributionList)

        name = "Dirichlet"

        # Compute exact indices
        exact = self.ComputeIndices(alpha)
        firstOrderIndices = ot.Point(exact["S"])
        totalOrderIndices = ot.Point(exact["T"])

        super(DirichletSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None
