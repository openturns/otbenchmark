#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define the g-sobol sensitivity benchmark problem."""

from otbenchmark.SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot


class GSobolSensitivity(SensitivityBenchmarkProblem):
    """Class to define the g-Sobol' sensitivity benchmark problem."""

    def __init__(self, a=[0.0, 9.0, 99.0]):
        """
        Create the g-Sobol sensitivity problem.

        The model is:

        g(x) = prod_{i=0,..., d-1} g[i](x[i])

        where d is the dimension and

        g[i](x[i]) = (|4 * x[i] - 2.0| + a[i])/ (1 + a[i])

        x[i] = Uniform(0.0, 1.0)

        for i = 0, ..., d-1.

        The default dimension is equal to 3.

        Parameters
        ----------
        a : sequence of floats
            The coefficients of the linear sum, with length d + 1.

        Example
        -------
        problem  = GSobolSensitivity()
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
