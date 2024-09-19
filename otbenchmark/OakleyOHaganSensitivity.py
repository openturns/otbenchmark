#!/usr/bin/python
# coding:utf-8
# Copyright 2021 EDF
"""Class to define a Oakley-O'Hagan sensitivity benchmark problem."""

from otbenchmark.SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot
import numpy as np


class OakleyOHaganSensitivity(SensitivityBenchmarkProblem):
    """Class to define a Oakley-O'Hagan sensitivity benchmark problem."""

    def __init__(self):
        """
        Create a Oakley-O'Hagan sensitivity problem.

        The function is defined by the equation:

        .. math::
            g(x) = x'Mx+a1'x + a2' sin(x) + a3'cos(x)

        where x1, ..., x15 ~ N(0, 1).

        The input random variables are independent.

        Examples
        --------
        >>> import otbenchmark as otb
        problem  = OakleyOHaganSensitivity()

        Notes
        -----
        The dimension and parameters of this problem cannot be changed.
        The Sobol' sensitivity indices are estimate with as
        much accuracy as possible.

        The model was first introduced in (Oakley, O'Hagan, 2004).

        The reference Sobol' indices were computed from a sparse
        polynomial chaos.
        A Sobol' low discrepancy design of experiments was generated
        with 500 training points.
        The sparse polynomial chaos expansion used an hyperbolic enumeration
        rule and a polynomial degree 6.
        The coefficients were estimated from regression.
        With 500 points in the validation set, the Q2 was greater than 98%.
        There are 2 significant digits in the reference results.

        References
        ----------
        * Oakley, J. E., & O'Hagan, A. (2004).
          Probabilistic sensitivity analysis of complex models:
          a Bayesian approach.
          Journal of the Royal Statistical Society:
          Series B (Statistical Methodology), 66(3), 751-769.

        * Derek Bingham, https://www.sfu.ca/~ssurjano/oakoh04.html
        """

        def OakleyOHaganFunction(X):
            y1 = a1.dot(X)
            y2 = a2.dot(np.sin(X))
            y3 = a3.dot(np.cos(X))
            Mx = M * X
            y4 = Mx.dot(X)
            y = y1 + y2 + y3 + y4
            return [y]

        dimension = 15
        M, a1, a2, a3 = self._getParameters()
        function = ot.PythonFunction(dimension, 1, OakleyOHaganFunction)
        function.setOutputDescription(["Y"])

        # Define the distribution
        distributionList = [ot.Normal(0.0, 1.0)] * dimension
        distribution = ot.ComposedDistribution(distributionList)

        name = "Oakley-O'Hagan"

        # Compute exact indices
        firstOrderIndices = ot.Point(
            [
                0.00,
                0.00,
                0.00,
                0.00,
                0.00,
                0.02,
                0.02,
                0.03,
                0.05,
                0.01,
                0.10,
                0.14,
                0.10,
                0.11,
                0.12,
            ]
        )
        totalOrderIndices = ot.Point(
            [
                0.06,
                0.06,
                0.04,
                0.05,
                0.02,
                0.04,
                0.06,
                0.08,
                0.10,
                0.04,
                0.15,
                0.15,
                0.14,
                0.14,
                0.16,
            ]
        )

        super(OakleyOHaganSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None

    def _getParameters(self):
        """Returns the parameters of the function"""
        M = np.array(
            [
                [
                    -2.2482886e-002,
                    -1.8501666e-001,
                    1.3418263e-001,
                    3.6867264e-001,
                    1.7172785e-001,
                    1.3651143e-001,
                    -4.4034404e-001,
                    -8.1422854e-002,
                    7.1321025e-001,
                    -4.4361072e-001,
                    5.0383394e-001,
                    -2.4101458e-002,
                    -4.5939684e-002,
                    2.1666181e-001,
                    5.5887417e-002,
                ],
                [
                    2.5659630e-001,
                    5.3792287e-002,
                    2.5800381e-001,
                    2.3795905e-001,
                    -5.9125756e-001,
                    -8.1627077e-002,
                    -2.8749073e-001,
                    4.1581639e-001,
                    4.9752241e-001,
                    8.3893165e-002,
                    -1.1056683e-001,
                    3.3222351e-002,
                    -1.3979497e-001,
                    -3.1020556e-002,
                    -2.2318721e-001,
                ],
                [
                    -5.5999811e-002,
                    1.9542252e-001,
                    9.5529005e-002,
                    -2.8626530e-001,
                    -1.4441303e-001,
                    2.2369356e-001,
                    1.4527412e-001,
                    2.8998481e-001,
                    2.3105010e-001,
                    -3.1929879e-001,
                    -2.9039128e-001,
                    -2.0956898e-001,
                    4.3139047e-001,
                    2.4429152e-002,
                    4.4904409e-002,
                ],
                [
                    6.6448103e-001,
                    4.3069872e-001,
                    2.9924645e-001,
                    -1.6202441e-001,
                    -3.1479544e-001,
                    -3.9026802e-001,
                    1.7679822e-001,
                    5.7952663e-002,
                    1.7230342e-001,
                    1.3466011e-001,
                    -3.5275240e-001,
                    2.5146896e-001,
                    -1.8810529e-002,
                    3.6482392e-001,
                    -3.2504618e-001,
                ],
                [
                    -1.2127800e-001,
                    1.2463327e-001,
                    1.0656519e-001,
                    4.6562296e-002,
                    -2.1678617e-001,
                    1.9492172e-001,
                    -6.5521126e-002,
                    2.4404669e-002,
                    -9.6828860e-002,
                    1.9366196e-001,
                    3.3354757e-001,
                    3.1295994e-001,
                    -8.3615456e-002,
                    -2.5342082e-001,
                    3.7325717e-001,
                ],
                [
                    -2.8376230e-001,
                    -3.2820154e-001,
                    -1.0496068e-001,
                    -2.2073452e-001,
                    -1.3708154e-001,
                    -1.4426375e-001,
                    -1.1503319e-001,
                    2.2424151e-001,
                    -3.0395022e-002,
                    -5.1505615e-001,
                    1.7254978e-002,
                    3.8957118e-002,
                    3.6069184e-001,
                    3.0902452e-001,
                    5.0030193e-002,
                ],
                [
                    -7.7875893e-002,
                    3.7456560e-003,
                    8.8685604e-001,
                    -2.6590028e-001,
                    -7.9325357e-002,
                    -4.2734919e-002,
                    -1.8653782e-001,
                    -3.5604718e-001,
                    -1.7497421e-001,
                    8.8699956e-002,
                    4.0025886e-001,
                    -5.5979693e-002,
                    1.3724479e-001,
                    2.1485613e-001,
                    -1.1265799e-002,
                ],
                [
                    -9.2294730e-002,
                    5.9209563e-001,
                    3.1338285e-002,
                    -3.3080861e-002,
                    -2.4308858e-001,
                    -9.9798547e-002,
                    3.4460195e-002,
                    9.5119813e-002,
                    -3.3801620e-001,
                    6.3860024e-003,
                    -6.1207299e-001,
                    8.1325416e-002,
                    8.8683114e-001,
                    1.4254905e-001,
                    1.4776204e-001,
                ],
                [
                    -1.3189434e-001,
                    5.2878496e-001,
                    1.2652391e-001,
                    4.5113625e-002,
                    5.8373514e-001,
                    3.7291503e-001,
                    1.1395325e-001,
                    -2.9479222e-001,
                    -5.7014085e-001,
                    4.6291592e-001,
                    -9.4050179e-002,
                    1.3959097e-001,
                    -3.8607402e-001,
                    -4.4897060e-001,
                    -1.4602419e-001,
                ],
                [
                    5.8107658e-002,
                    -3.2289338e-001,
                    9.3139162e-002,
                    7.2427234e-002,
                    -5.6919401e-001,
                    5.2554237e-001,
                    2.3656926e-001,
                    -1.1782016e-002,
                    7.1820601e-002,
                    7.8277291e-002,
                    -1.3355752e-001,
                    2.2722721e-001,
                    1.4369455e-001,
                    -4.5198935e-001,
                    -5.5574794e-001,
                ],
                [
                    6.6145875e-001,
                    3.4633299e-001,
                    1.4098019e-001,
                    5.1882591e-001,
                    -2.8019898e-001,
                    -1.6032260e-001,
                    -6.8413337e-002,
                    -2.0428242e-001,
                    6.9672173e-002,
                    2.3112577e-001,
                    -4.4368579e-002,
                    -1.6455425e-001,
                    2.1620977e-001,
                    4.2702105e-003,
                    -8.7399014e-002,
                ],
                [
                    3.1599556e-001,
                    -2.7551859e-002,
                    1.3434254e-001,
                    1.3497371e-001,
                    5.4005680e-002,
                    -1.7374789e-001,
                    1.7525393e-001,
                    6.0258929e-002,
                    -1.7914162e-001,
                    -3.1056619e-001,
                    -2.5358691e-001,
                    2.5847535e-002,
                    -4.3006001e-001,
                    -6.2266361e-001,
                    -3.3996882e-002,
                ],
                [
                    -2.9038151e-001,
                    3.4101270e-002,
                    3.4903413e-002,
                    -1.2121764e-001,
                    2.6030714e-002,
                    -3.3546274e-001,
                    -4.1424111e-001,
                    5.3248380e-002,
                    -2.7099455e-001,
                    -2.6251302e-002,
                    4.1024137e-001,
                    2.6636349e-001,
                    1.5582891e-001,
                    -1.8666254e-001,
                    1.9895831e-002,
                ],
                [
                    -2.4388652e-001,
                    -4.4098852e-001,
                    1.2618825e-002,
                    2.4945112e-001,
                    7.1101888e-002,
                    2.4623792e-001,
                    1.7484502e-001,
                    8.5286769e-003,
                    2.5147070e-001,
                    -1.4659862e-001,
                    -8.4625150e-002,
                    3.6931333e-001,
                    -2.9955293e-001,
                    1.1044360e-001,
                    -7.5690139e-001,
                ],
                [
                    4.1494323e-002,
                    -2.5980564e-001,
                    4.6402128e-001,
                    -3.6112127e-001,
                    -9.4980789e-001,
                    -1.6504063e-001,
                    3.0943325e-003,
                    5.2792942e-002,
                    2.2523648e-001,
                    3.8390366e-001,
                    4.5562427e-001,
                    -1.8631744e-001,
                    8.2333995e-003,
                    1.6670803e-001,
                    1.6045688e-001,
                ],
            ]
        )
        a1 = np.array(
            [
                0.0118,
                0.0456,
                0.2297,
                0.0393,
                0.1177,
                0.3865,
                0.3897,
                0.6061,
                0.6159,
                0.4005,
                1.0741,
                1.1474,
                0.7880,
                1.1242,
                1.1982,
            ]
        )

        a2 = np.array(
            [
                0.4341,
                0.0887,
                0.0512,
                0.3233,
                0.1489,
                1.0360,
                0.9892,
                0.9672,
                0.8977,
                0.8083,
                1.8426,
                2.4712,
                2.3946,
                2.0045,
                2.2621,
            ]
        )
        a3 = np.array(
            [
                0.1044,
                0.2057,
                0.0774,
                0.2730,
                0.1253,
                0.7526,
                0.8570,
                1.0331,
                0.8388,
                0.7970,
                2.2145,
                2.0382,
                2.4004,
                2.0541,
                1.9845,
            ]
        )
        M = ot.Matrix(M)
        a1 = ot.Point(a1)
        a2 = ot.Point(a2)
        a3 = ot.Point(a3)
        return M, a1, a2, a3
