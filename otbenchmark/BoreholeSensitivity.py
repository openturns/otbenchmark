#!/usr/bin/python
# coding:utf-8
# Copyright 2020 - 2021 EDF
"""Class to define a Borehole sensitivity benchmark problem."""

from otbenchmark.SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot


class BoreholeSensitivity(SensitivityBenchmarkProblem):
    """Class to define a Borehole sensitivity benchmark problem."""

    def __init__(self):
        """
        Create a Borehole sensitivity problem.

        The function is defined by the equation:

        g(x) = (2*pi_*Tu*(Hu-Hl))/(ln(r/rw)*(1+(2*L*Tu)/(ln(r/rw)*rw^2*Kw)+Tu/Tl))

        where:

        * r_w: radius of borehole (m)
        * r: radius of influence (m)
        * T_u: transmissivity of upper aquifer (m^2/yr)
        * H_u: potentiometric head of upper aquifer (m)
        * T_l: transmissivity of lower aquifer (m^2/yr)
        * H_l: potentiometric head of lower aquifer (m)
        * L: length of borehole (m)
        * K_w: hydraulic conductivity of borehole (m/yr)

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
        With 1000  points in the validation set, the Q2 was greater than 99.9%.
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
            ["(2*pi_*Tu*(Hu-Hl))/(ln(r/rw)*(1+(2*L*Tu)/(ln(r/rw)*rw^2*Kw)+Tu/Tl))"],
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
        distribution = ot.ComposedDistribution(coll)
        distribution.setDescription(input_names)

        name = "Borehole"

        # Compute exact indices
        firstOrderIndices = ot.Point([0.66, 0.00, 0.00, 0.09, 0.00, 0.09, 0.09, 0.02])
        totalOrderIndices = ot.Point([0.69, 0.00, 0.00, 0.11, 0.00, 0.11, 0.10, 0.02])

        super(BoreholeSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None
