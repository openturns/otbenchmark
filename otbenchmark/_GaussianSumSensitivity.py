#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define a gaussian sum sensitivity benchmark problem."""

from ._SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot


class GaussianSumSensitivity(SensitivityBenchmarkProblem):
    """Class to define a gaussian sum sensitivity benchmark problem."""

    def __init__(self, a=[1.0] * 3, mu=[0.0] * 2, sigma=[1.0] * 2):
        r"""
        Create a gaussian sum sensitivity problem.

        The model is:

        .. math::

           g(\boldsymbol{x}) = a_0 + a_1 x_1 + a_2 x_2
               + \dots + a_d x_d

        for any :math:`\boldsymbol{x} \in \mathbb{R}^d` where
        :math:`a_0, a_1, a_2, \ldots, a_d \in \mathbb{R}` are
        constant parameters.
        We assume that the input random variables have Gaussian distributions:

        .. math::

           X_i \sim \mathcal{N}\left(\mu_i,\ \sigma_i^2\right)

        for :math:`i \in \{1, \dots, d\}`.

        The output variance is:

        .. math::

           \operatorname{Var}(Y) = a_1^2 \, \sigma_1^2
               + a_2^2 \, \sigma_2^2
               + \dots + a_d^2 \, \sigma_d^2

        The first-order Sobol' indices are:

        .. math::

           S_i = \frac{a_{i}^{2}\, \sigma_{i}^{2}}{\operatorname{Var}(Y)}

        for :math:`i = 1, \dots, d`.

        The total Sobol' sensitivity indices are equal to the
        first order indices.

        Parameters
        ----------
        a : sequence of floats
            The coefficients of the linear sum, with length d + 1.

        mu : sequence of floats
            The mean of the gaussian distributions, with length d.

        sigma : sequence of floats
            The standard deviations of the gaussian distributions, with length d.

        Examples
        --------
        >>> import otbenchmark as otb
        >>> problem = otb.GaussianSumSensitivity()
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
