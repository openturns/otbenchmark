#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define a linear sum sensitivity benchmark problem."""

from otbenchmark.SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot


class GaussianProductSensitivity(SensitivityBenchmarkProblem):
    """Class to define a linear sum sensitivity benchmark problem."""

    def __init__(self, mu=[0.0] * 2, sigma=[1.0] * 2):
        """
        Create a gaussian product sensitivity problem.

        The model is:

        g(x) = x[0] * x[1] * ... * x[d-1]

        where d is the dimension and

        x[i] = Normal(mu[i], sigma[i])

        for i = 0, ..., d-1.

        The default dimension is equal to 2.

        This case is interesting because interactions matters.

        References
        ----------
        * "Sensitivity analysis examples with NISP"
          Michael Baudin (INRIA), Jean-Marc Martinez (CEA)

        Parameters
        ----------
        mu : sequence of floats
            The mean of the gaussian distributions, with length d.

        sigma : sequence of floats
            The standard deviations of the gaussian distributions, with length d.

        Example
        -------
        problem  = LinearSumSensitivity()
        """

        dimension = len(mu)

        dimensionsigma = len(sigma)
        if dimension != dimensionsigma:
            raise ValueError(
                "The dimension of sigma is equal to %d, "
                "which is different from %d." % (dimensionsigma, dimension)
            )

        # Define the function

        def ProductModel(X):
            X = ot.Point(X)
            d = X.getDimension()
            Y = 1.0
            for i in range(d):
                Y *= X[i]
            return ot.Point([Y])

        function = ot.PythonFunction(dimension, 1, ProductModel)

        # Define the distribution
        distributionList = [ot.Normal(mu[i], sigma[i]) for i in range(dimension)]
        distribution = ot.ComposedDistribution(distributionList)

        name = "GaussianProduct"

        # Compute variance
        varY = 1.0
        muproduct = 1.0
        for i in range(dimension):
            varY *= mu[i] ** 2 + sigma[i] ** 2
            muproduct *= mu[i] ** 2
        varY -= muproduct
        # Compute exact indices
        firstOrderIndices = ot.Point(dimension)
        totalOrderIndices = ot.Point(firstOrderIndices)
        for i in range(dimension):
            # Compute first order
            product = 1.0
            for j in range(dimension):
                if j != i:
                    product *= mu[j] ** 2
                firstOrderIndices[i] = product * sigma[i] ** 2 / varY
            # Compute total order
            product = 1.0
            for j in range(dimension):
                if j != i:
                    product *= mu[j] ** 2 + sigma[j] ** 2
            totalOrderIndices[i] = 1.0 - (mu[i] ** 2 * product - muproduct) / varY

        super(GaussianProductSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None
