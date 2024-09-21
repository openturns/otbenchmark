#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define the g-sobol sensitivity benchmark problem."""

from ._SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot


class GSobolSensitivity(SensitivityBenchmarkProblem):
    """Class to define the g-Sobol' sensitivity benchmark problem."""

    def __init__(self, a=[0.0, 9.0, 99.0]):
        """
        Create the g-Sobol sensitivity problem.

        The model is:

        g(x) = prod_{i=0,..., d-1} g_i(x_i)

        where d is the dimension and

        .. math::
            g_i(x_i) = (|4 * x_i - 2.0| + a_i)/ (1 + a_i)

        x_i = Uniform(0.0, 1.0)

        for i = 0, ..., d-1.
        The input random variables are independent.

        The default dimension is equal to 3.

        Parameters
        ----------
        a : sequence of floats
            The coefficients of the linear sum, with length d + 1.

        Examples
        --------
        >>> import otbenchmark as otb
        >>> problem = otb.GSobolSensitivity()

        Notes
        -----

        The dimension of the problem can be changed.
        The exact sensitivity indices are computed from the vector a.

        The function g has no derivative at X=(1/2,..., 1/2).
        The function g is symmetric with respect to X=(1/2,..., 1/2).

        When a[i] increases, the variable X[i] has a first order
        indice closer to zero.

        The detailed analysis is the following:
        * if a[i] = 0, then the variable X[i] is ”important”,
        since 0 ≤ gi (x) ≤ 2.
        * if a[i] = 9, then the variable X[i] is ”non important”,
        since 0.90 ≤ gi (x) ≤ 1.10.
        * if a[i] = 99, then the variable X[i] is ”non significant”,
        since 0.99 ≤ gi (x) ≤ 1.01.

        The model was first introduced in (Saltelli, Sobol', 1995).

        References
        ----------
        Saltelli, A., & Sobol', I. Y. M. (1994).
        Sensitivity analysis for nonlinear mathematical models: numerical experience.
        Matematicheskoe Modelirovanie, 7(11), 16-28.

        Saltelli, A., & Sobol', I. M. (1995). About the use of rank transformation
        in sensitivity analysis of model output.
        Reliability Engineering & System Safety, 50(3), 225-239.

        Marrel, A., Iooss, B., Van Dorpe, F., & Volkova, E. (2008).
        An efficient methodology for modeling complex computer codes with
        Gaussian processes.
        Computational Statistics & Data Analysis, 52(10), 4731-4744.

        Saltelli, A., Chan, K., & Scott, E. M. (Eds.). (2000).
        Sensitivity analysis (Vol. 134). New York: Wiley.
        """

        dimension = len(a)

        # Define the function

        def GSobolModel(X):
            X = ot.Point(X)
            d = X.getDimension()
            Y = 1.0
            for i in range(d):
                Y *= (abs(4.0 * X[i] - 2.0) + a[i]) / (1.0 + a[i])
            return ot.Point([Y])

        function = ot.PythonFunction(dimension, 1, GSobolModel)
        function.setOutputDescription(["Y"])

        # Define the distribution
        distributionList = [ot.Uniform(0.0, 1.0) for i in range(dimension)]
        distribution = ot.ComposedDistribution(distributionList)

        name = "GSobol"

        # Compute variance
        varY = 1.0
        for i in range(dimension):
            varY *= 1.0 + 1.0 / (3.0 * (1.0 + a[i]) ** 2)
        varY -= 1.0
        # Compute exact indices
        firstOrderIndices = ot.Point(dimension)
        totalOrderIndices = ot.Point(dimension)
        for i in range(dimension):
            p = 1.0 / (3.0 * (1.0 + a[i]) ** 2)
            firstOrderIndices[i] = p / varY
            totalOrderIndices[i] = 1.0 - ((varY + 1.0) / (1.0 + p) - 1.0) / varY

        super(GSobolSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None
