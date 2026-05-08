#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define a linear sum sensitivity benchmark problem."""

from ._SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot


class GaussianProductSensitivity(SensitivityBenchmarkProblem):
    """Class to define a linear sum sensitivity benchmark problem."""

    def __init__(self, mu=[0.0] * 2, sigma=[1.0] * 2):
        r"""
        Create a gaussian product sensitivity problem.

        .. math::

           g(\boldsymbol{x}) = x_1 \, x_2 \, \cdots \, x_d

        for any :math:`\boldsymbol{x} \in \mathbb{R}^d`.
        We assume that the input random variables have Gaussian distributions:

        .. math::

           X_i \sim \mathcal{N}\left(\mu_i,\ \sigma_i^2\right)

        for :math:`i \in \{1, \dots, d\}`.

        The default dimension is :math:`d = 2`.

        The variance of the model output is:

        .. math::

            \text{Var}(Y) = \prod_{i=1}^{d} \left(\mu_i^2 + \sigma_i^2\right)
                - \prod_{i=1}^{d} \mu_i^2

        The first order Sobol' index for the :math:`i`-th variable is:

        .. math::

            S_i = \frac{\sigma_i^2 \prod_{j=1, j \neq i}^{d} \mu_j^2}{\text{Var}(Y)}

        The total order Sobol' index for the :math:`i`-th variable is:

        .. math::

            S_{T_i} = 1 - \frac{\mu_i^2
                \prod_{j=1, j \neq i}^{d} \left(\mu_j^2 + \sigma_j^2\right)
                    - \prod_{j=1}^{d} \mu_j^2}{\text{Var}(Y)}

        This case is interesting because interactions matters.

        References
        ----------
        * "Sensitivity analysis examples with NISP", Michael Baudin (INRIA), Jean-Marc Martinez (CEA)

        Parameters
        ----------
        mu : sequence of floats
            The mean of the gaussian distributions, with length d.

        sigma : sequence of floats
            The standard deviations of the gaussian distributions, with length d.

        Examples
        --------
        >>> import otbenchmark as otb
        >>> problem = otb.LinearSumSensitivity()
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
        distribution = ot.JointDistribution(distributionList)

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
