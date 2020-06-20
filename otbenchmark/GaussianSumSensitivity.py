#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define a gaussian sum sensitivity benchmark problem."""

from otbenchmark.SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot


class GaussianSumSensitivity(SensitivityBenchmarkProblem):
    """Class to define a gaussian sum sensitivity benchmark problem."""

    def __init__(self, a=[1.0] * 3, mu=[0.0] * 2, sigma=[1.0] * 2):
        """
        Create a gaussian sum sensitivity problem.

        The model is:

        g(x) = a[0] + a[1] * x[0] + a[2] * x[1] + ... + a[d] * x[d-1]

        where d is the dimension and

        x[i] = Normal(mu[i], sigma[i])

        for i = 0, ..., d-1.

        The default dimension is equal to 2.

        The variance of the output is

        V(Y) = a[1]^2 * sigma[0]^2 + ... + a[d]^2 * sigma[d-1]^2

        The first order indices are

        S[i] = (a[i + 1]^2 * sigma[i]^2) / V(Y)

        for i=0,1,...,dimension.

        The total sensitivity indices are equal to the
        first order indices.

        Parameters
        ----------
        a : sequence of floats
            The coefficients of the linear sum, with length d + 1.

        mu : sequence of floats
            The mean of the gaussian distributions, with length d.

        sigma : sequence of floats
            The standard deviations of the gaussian distributions, with length d.

        Example
        -------
        problem  = GaussianSumSensitivity()
        """

        dimension = len(a) - 1

        dimensionmu = len(mu)
        if dimension != dimensionmu:
            raise ValueError(
                "The dimension of mu is equal to %d, "
                "which is different from %d." % (dimensionmu, dimension)
            )
        dimensionsigma = len(sigma)
        if dimension != dimensionsigma:
            raise ValueError(
                "The dimension of sigma is equal to %d, "
                "which is different from %d." % (dimensionsigma, dimension)
            )

        # Define the function

        def LinearSumModel(X):
            X = ot.Point(X)
            d = X.getDimension()
            Y = a[0]
            for i in range(d):
                Y += a[i + 1] * X[i]
            return ot.Point([Y])

        function = ot.PythonFunction(dimension, 1, LinearSumModel)

        # Define the distribution
        distributionList = [ot.Normal(mu[i], sigma[i]) for i in range(dimension)]
        distribution = ot.ComposedDistribution(distributionList)

        name = "GaussianSum"

        # Compute variance
        varY = 0.0
        for i in range(dimension):
            varY += a[i + 1] ** 2 * sigma[i] ** 2
        # Compute exact indices
        firstOrderIndices = ot.Point(dimension)
        for i in range(dimension):
            firstOrderIndices[i] = a[i + 1] ** 2 * sigma[i] ** 2 / varY
        totalOrderIndices = ot.Point(firstOrderIndices)

        super(GaussianSumSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None
