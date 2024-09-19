#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The non-monotonic function of Morris f: R^20 -> R.
"""
from otbenchmark.SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot
import warnings


class MorrisFunction(ot.OpenTURNSPythonFunction):
    """
    The non-monotonic function of Morris f: [0,1]^20 -> R

    References
    ---------
    M. D. Morris, 1991, Factorial sampling plans for preliminary
    computational experiments,Technometrics, 33, 161--174.

    This code was taken from otmorris/python/src/Morris.i.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(123)
    >>> b0 = ot.DistFunc.rNormal()
    >>> alpha = ot.DistFunc.rNormal(10)
    >>> beta =  ot.DistFunc.rNormal(6*14)
    >>> gamma =  ot.DistFunc.rNormal(20*14)
    >>> f = ot.Function( MorrisFunction(alpha, beta, gamma, b0) )
    >>> input_sample = ot.ComposedDistribution([ot.Uniform(0,1)] * 20).getSample(20)
    >>> output_sample = f(input_sample)
    """

    def __init__(
        self, alpha=ot.Point(10), beta=ot.Point(14 * 6), gamma=ot.Point(20 * 14), b0=0.0
    ):
        """
        Create the Morris function

        Parameters
        ----------
        alpha : ot.Point(10), optional
            The linear part. The default is ot.Point(10).
        beta : ot.Point(14 * 6), optional
            A segment of the quadratic coefficients. The default is ot.Point(14 * 6).
        gamma : ot.Point(20 * 14), optional
            A segment of the quadratic coefficients. The default is ot.Point(20 * 14).
        b0 : float, optional
            The constant part. The default is 0.0.

        Returns
        -------
        None.

        """
        ot.OpenTURNSPythonFunction.__init__(self, 20, 1)
        self.b0 = float(b0)
        # Check alpha dimension
        assert len(alpha) == 10
        self.b1 = [20.0] * 10 + list(alpha)
        # Check beta and gamma dimension
        assert len(beta) == 6 * 14
        assert len(gamma) == 20 * 14
        self.b2 = [[0.0] * 20] * 20
        for i in range(6):
            for j in range(6):
                self.b2[i][j] = -15.0
        # Take into account beta
        k = 0
        for i in range(6):
            for j in range(14):
                self.b2[i][j + 6] = beta[k]
                k = k + 1
        # Take into account gamma
        k = 0
        for i in range(6, 20):
            for j in range(20):
                self.b2[i][j] = gamma[k]

        # b3
        self.b3 = [[[0.0] * 20] * 20] * 20
        for i in range(5):
            for j in range(5):
                for k in range(5):
                    self.b3[i][j][k] = -10.0
        # b4
        self.b4 = [[[[0.0] * 20] * 20] * 20] * 20
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    for ell in range(4):
                        self.b4[i][j][k][ell] = 5.0

    def _exec(self, x):
        assert len(x) == 20
        b1 = self.b1
        b2 = self.b2
        b3 = self.b3
        b4 = self.b4
        # X is a list, transform it into array
        X = ot.Point(x)
        w = (X - [0.5] * 20) * 2
        for k in [2, 4, 6]:
            w[k] = 2.0 * (1.1 * X[k] / (X[k] + 0.1) - 0.5)
        y = self.b0
        y = w.dot(b1)
        # Morris function
        for i in range(19):
            for j in range(i + 1, 20):
                y += b2[i][j] * w[i] * w[j]
        for i in range(18):
            for j in range(i + 1, 19):
                for k in range(j + 1, 20):
                    y += b3[i][j][k] * w[i] * w[j] * w[k]

        for i in range(17):
            for j in range(i + 1, 18):
                for k in range(j + 1, 20):
                    for ell in range(k + 1, 20):
                        y += b4[i][j][k][ell] * w[i] * w[j] * w[k] * w[ell]

        return [y]


class MorrisSensitivity(SensitivityBenchmarkProblem):
    """Class to define the Morris sensitivity benchmark problem."""

    def __init__(self, random_parameters=False):
        """
        Define the Morris sensitivity benchmark problem.

        The function g is from [0,1]^20 to R.

        Its input distribution are Uniform([0, 1]) random variables.
        The input random variables are independent.

        It is defined as the sum:

        g(x) = beta_0
        + sum_i beta[i] * w[i](x)
        + sum_{ij} beta[i, j] * w[i](x) * w[j](x)
        + sum_{ijk} beta[i, j, k] * w[i](x) * w[j](x) * w[k](x)
        + sum_{ijkl} beta[i, j, k, l] * w[i](x) * w[j](x) * w[k](x) * w[l](x)

        where

        w[i](x) = 2 * (x[i] - 0.5) for 𝑖=1,2,4,6,8,...,20

        and

        w[i](x) = 2 * (1.1 * x[i] / (x[i] + 1) - 0.5) for 𝑖=3,5,7.

        In order to get consistent results, the default value of the
        random_parameters parameter is so that the parameters beta
        are constant, deterministic, values.

        Parameters
        ----------
        random_parameters: bool
            Set to True to get random parameters.

        Returns
        -------
        None.

        Notes
        -----

        The dimension of this problem is equal to 20 and cannot be changed.

        The function is the sum of five functions.
        * The first is constant and equal to beta_0.
        * The second is a linear combination of w[i] coefficients.
        * The third is a order 2 combination of w[i] coefficients.
        * The fourth is a order 3 combination of w[i] coefficients.
        * The fifth is a order 4 combination of w[i] coefficients.

        Therefore, Morris's function is an order 4 polynomial.

        This code was taken from otmorris/python/src/Morris.i.

        The reference Sobol' indices were computed from a sparse
        polynomial chaos.
        A Sobol' low discrepancy design of experiments was generated
        with 500 training points.
        The sparse polynomial chaos expansion used an hyperbolic enumeration
        rule and a polynomial degree 4.
        The coefficients were estimated from regression.
        With 500 points in the validation set, the Q2 was greater than 98%.
        There are 2 significant digits in the reference results.

        References
        ----------
        M. D. Morris, 1991, Factorial sampling plans for preliminary
        computational experiments,Technometrics, 33, 161--174.
        """
        # Define the function
        dimension = 20
        if random_parameters:
            b0 = ot.DistFunc.rNormal()
            alpha = ot.DistFunc.rNormal(10)
            beta = ot.DistFunc.rNormal(6 * 14)
            gamma = ot.DistFunc.rNormal(20 * 14)
            warnings.warn(
                "The parameters were changed, but the reference Sobol' "
                "indices are not updated."
            )
        else:
            b0, alpha, beta, gamma = self._get_parameters()

        function = ot.Function(MorrisFunction(alpha, beta, gamma, b0))
        # Define the distribution
        distributionList = [ot.Uniform(0.0, 1.0) for i in range(dimension)]
        distribution = ot.ComposedDistribution(distributionList)

        name = "Morris"

        firstOrderIndices = ot.Point(
            [
                0.08,
                0.08,
                0.06,
                0.08,
                0.06,
                0.13,
                0.06,
                0.13,
                0.13,
                0.12,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
            ]
        )
        totalOrderIndices = ot.Point(
            [
                0.11,
                0.11,
                0.06,
                0.11,
                0.06,
                0.13,
                0.06,
                0.13,
                0.13,
                0.12,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
            ]
        )
        super(MorrisSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None

    def _get_parameters(self):
        b0 = 0.60820165121876457
        alpha = ot.Point(
            [
                -1.26617310,
                -0.43826562,
                1.20547820,
                -2.18138523,
                0.35004209,
                -0.35500705,
                1.43724931,
                0.81066798,
                0.79315601,
                -0.47052560,
            ]
        )
        beta = ot.Point(
            [
                0.26,
                -2.29,
                -1.28,
                -1.31,
                -0.09,
                1.00,
                -0.14,
                -0.56,
                0.45,
                0.32,
                0.45,
                -1.04,
                -0.86,
                0.47,
                -0.13,
                0.35,
                1.78,
                0.07,
                -0.78,
                -0.72,
                -0.24,
                -1.79,
                0.40,
                1.37,
                1.00,
                0.74,
                -0.04,
                0.54,
                0.30,
                0.41,
                -0.49,
                -0.38,
                -0.75,
                0.26,
                1.97,
                -0.67,
                1.86,
                0.05,
                0.79,
                0.72,
                -0.74,
                0.18,
                -1.53,
                0.66,
                0.54,
                1.74,
                -0.96,
                0.38,
                -0.18,
                1.67,
                -1.04,
                -0.35,
                1.21,
                -0.78,
                -1.37,
                0.10,
                -0.89,
                0.91,
                0.33,
                -0.48,
                0.68,
                1.71,
                1.07,
                -0.51,
                -1.66,
                2.25,
                0.76,
                -0.51,
                -0.63,
                -0.96,
                0.54,
                0.81,
                -0.73,
                -0.11,
                0.99,
                -0.16,
                -0.94,
                -1.97,
                -0.66,
                0.34,
                1.02,
                0.64,
                -0.09,
                -0.86,
            ]
        )
        gamma = ot.Point(
            [
                1.3,
                -0.2,
                1.3,
                2.1,
                -0.9,
                -1.5,
                -1.3,
                0.2,
                -3.1,
                0.0,
                -1.3,
                1.0,
                -0.8,
                0.2,
                1.0,
                0.3,
                -0.5,
                -0.5,
                0.3,
                -0.2,
                3.0,
                0.9,
                0.6,
                0.6,
                -1.5,
                -2.4,
                0.7,
                -0.7,
                -0.8,
                0.4,
                -0.5,
                1.9,
                0.2,
                1.7,
                -0.5,
                -0.7,
                -0.5,
                -2.3,
                -0.6,
                -0.3,
                -1.8,
                -0.7,
                0.1,
                0.9,
                -1.5,
                -0.3,
                1.3,
                -0.4,
                -1.9,
                -0.5,
                0.6,
                0.0,
                0.7,
                -0.2,
                0.5,
                -0.0,
                -0.0,
                0.1,
                -0.4,
                -0.1,
                0.1,
                -0.2,
                0.5,
                0.2,
                0.4,
                0.1,
                -0.1,
                1.5,
                1.2,
                0.5,
                -0.7,
                -0.1,
                -1.5,
                1.2,
                0.9,
                -0.3,
                0.6,
                -0.6,
                -1.4,
                -0.5,
                -1.6,
                0.5,
                0.2,
                -0.1,
                0.6,
                -0.6,
                -1.2,
                -0.9,
                -0.1,
                0.4,
                0.5,
                -1.5,
                -0.7,
                0.7,
                -1.4,
                -0.0,
                -0.6,
                -0.3,
                2.1,
                1.2,
                -1.5,
                -0.8,
                -0.3,
                0.4,
                -0.8,
                0.9,
                -0.9,
                -0.9,
                1.2,
                0.3,
                0.5,
                0.5,
                -0.8,
                -0.7,
                -0.1,
                -1.0,
                -1.2,
                1.4,
                -0.6,
                -1.7,
                0.8,
                3.0,
                1.7,
                -1.6,
                -1.0,
                0.8,
                -0.5,
                -0.0,
                -0.4,
                -0.3,
                -0.9,
                -2.5,
                -0.1,
                -0.0,
                0.6,
                0.1,
                -0.7,
                -0.5,
                0.6,
                -0.5,
                -2.2,
                -0.4,
                0.3,
                -0.4,
                1.1,
                -0.0,
                0.5,
                -0.6,
                -1.6,
                -0.5,
                -0.3,
                0.0,
                0.6,
                0.8,
                0.9,
                1.5,
                0.7,
                1.4,
                0.6,
                1.9,
                0.9,
                -0.9,
                -0.5,
                -0.6,
                1.3,
                -2.3,
                0.4,
                -1.0,
                -1.1,
                0.1,
                0.7,
                -1.1,
                -0.0,
                0.6,
                -0.0,
                0.1,
                -0.2,
                -1.3,
                -1.0,
                -1.7,
                0.9,
                -0.5,
                -1.0,
                -1.4,
                1.9,
                0.8,
                1.1,
                0.7,
                -0.5,
                0.6,
                0.7,
                0.7,
                0.5,
                -0.4,
                1.5,
                -0.4,
                0.5,
                1.5,
                -0.3,
                -1.4,
                1.3,
                -0.5,
                -0.3,
                -0.3,
                -0.8,
                1.7,
                0.9,
                1.3,
                -0.6,
                -0.0,
                1.9,
                0.4,
                -1.3,
                -1.2,
                -0.4,
                -0.8,
                -0.7,
                0.4,
                -0.6,
                -0.6,
                0.1,
                -0.1,
                0.8,
                -0.7,
                0.7,
                0.6,
                -2.2,
                -0.8,
                -0.7,
                -0.1,
                0.6,
                0.7,
                0.7,
                -1.2,
                0.9,
                1.0,
                0.1,
                0.5,
                -1.7,
                0.4,
                0.7,
                -0.5,
                -0.5,
                1.3,
                1.6,
                1.9,
                0.4,
                0.2,
                0.2,
                0.6,
                -0.4,
                0.6,
                -2.2,
                0.4,
                0.8,
                -0.5,
                -0.3,
                -1.2,
                0.0,
                -1.2,
                0.1,
                0.7,
                -0.3,
                -0.4,
                0.3,
                -1.5,
                1.1,
                0.4,
                -0.2,
                0.4,
                0.9,
                1.7,
                -0.7,
                1.7,
                0.4,
                -0.3,
                0.4,
                0.4,
                0.2,
                1.4,
            ]
        )
        return b0, alpha, beta, gamma
