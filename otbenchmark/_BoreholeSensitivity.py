#!/usr/bin/python
# coding:utf-8
# Copyright 2020 - 2021 EDF
"""Class to define a Borehole sensitivity benchmark problem."""

from ._SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot


class BoreholeSensitivity(SensitivityBenchmarkProblem):
    """Class to define a Borehole sensitivity benchmark problem."""

    def __init__(self):
        r"""
        Create a Borehole sensitivity problem.

        The function is defined by the equation:

        .. math::

            g(\boldsymbol{x})
            = \frac{2\pi\, T_u\, (H_u - H_\ell)}{\ln\!\left(\frac{r}{r_w}\right)\left(1 + \frac{2 L T_u}
                {\ln\!\left(\frac{r}{r_w}\right) r_w^{2} K_w} + \frac{T_u}{T_\ell}\right)}

        where :math:`\boldsymbol{x} = (r_w, r, T_u, H_u, T_\ell, H_\ell, L, K_w)^\top`
        and :

        * :math:`r_w`: radius of borehole (m);
        * :math:`r`: radius of influence (m);
        * :math:`T_u`: transmissivity of upper aquifer (m²/yr);
        * :math:`H_u`: potentiometric head of upper aquifer (m);
        * :math:`T_\ell`: transmissivity of lower aquifer (m²/yr);
        * :math:`H_\ell`: potentiometric head of lower aquifer (m);
        * :math:`L`: length of borehole (m);
        * :math:`K_w`: hydraulic conductivity of borehole (m/yr).

        The next table presents the marginal distributions of
        each random variable in the model.

        .. table::
            :widths: auto

            +---------------+-------------+------------------------------------------+
            | Variable      | Distribution| Parameters                               |
            +===============+=============+==========================================+
            | :math:`r_w`   | Normal      | μ = 0.1, σ = 0.0161812                   |
            +---------------+-------------+------------------------------------------+
            | :math:`r`     | Log-Normal  | μ_log = 7.71, σ_log = 1.0056             |
            +---------------+-------------+------------------------------------------+
            | :math:`T_u`   | Uniform     | a = 63,070, b = 115,600                  |
            +---------------+-------------+------------------------------------------+
            | :math:`H_u`   | Uniform     | a = 990, b = 1,110                       |
            +---------------+-------------+------------------------------------------+
            | :math:`T_\ell`| Uniform     | a = 63.1, b = 116                        |
            +---------------+-------------+------------------------------------------+
            | :math:`H_\ell`| Uniform     | a = 700, b = 820                         |
            +---------------+-------------+------------------------------------------+
            | :math:`L`     | Uniform     | a = 1,120, b = 1,680                     |
            +---------------+-------------+------------------------------------------+
            | :math:`K_w`   | Uniform     | a = 9,855, b = 12,045                    |
            +---------------+-------------+------------------------------------------+

        The input random variables are independent.

        Parameters
        ----------
        None.

        Examples
        --------
        >>> import otbenchmark as otb
        >>> problem = otb.FloodingSensitivity()

        Notes
        -----
        The dimension of this problem cannot be changed.

        The reference Sobol' indices were computed from a sparse
        polynomial chaos.
        A Sobol' low discrepancy design of experiments was generated
        with 1000 training points.
        The sparse polynomial chaos expansion used an hyperbolic enumeration
        rule and a polynomial degree 6.
        The coefficients were estimated from regression.
        With 1000  points in the validation set, the Q² was greater than 99.9%.
        There are 2 significant digits in the reference results.

        References
        ----------
        * Worley, B. A. (1987). Deterministic uncertainty analysis
          (No. CONF-871101-30). Oak Ridge National Lab., TN (USA).

        * Morris, M. D., Mitchell, T. J., & Ylvisaker, D. (1993).
          Bayesian design and analysis of computer experiments:
          use of derivatives in surface prediction.
          Technometrics, 35(3), 243-255.
        """

        input_names = ["rw", "r", "Tu", "Hu", "Tl", "Hl", "L", "Kw"]
        function = ot.SymbolicFunction(
            input_names,
            [
                "(2 * pi_ * Tu * (Hu - Hl)) / (ln(r / rw) * (1 + (2 * L * Tu) / (ln(r / rw) * rw^2 * Kw) + Tu / Tl))"
            ],
        )
        coll = [
            ot.Normal(0.1, 0.0161812),
            ot.LogNormal(7.71, 1.0056),
            ot.Uniform(63070.0, 115600.0),
            ot.Uniform(990.0, 1110.0),
            ot.Uniform(63.1, 116.0),
            ot.Uniform(700.0, 820.0),
            ot.Uniform(1120.0, 1680.0),
            ot.Uniform(9855.0, 12045.0),
        ]
        distribution = ot.JointDistribution(coll)
        distribution.setDescription(input_names)

        name = "Borehole"

        # Compute exact indices
        firstOrderIndices = ot.Point([0.66, 0.00, 0.00, 0.09, 0.00, 0.09, 0.09, 0.02])
        totalOrderIndices = ot.Point([0.69, 0.00, 0.00, 0.11, 0.00, 0.11, 0.10, 0.02])

        super(BoreholeSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None
