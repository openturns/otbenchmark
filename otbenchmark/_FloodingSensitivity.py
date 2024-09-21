#!/usr/bin/python
# coding:utf-8
# Copyright 2020 - 2021 EDF
"""Class to define a Flooding sensitivity benchmark problem."""

from ._SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot


class FloodingSensitivity(SensitivityBenchmarkProblem):
    """Class to define a Flooding sensitivity benchmark problem."""

    def __init__(self):
        """
        Create a Flooding sensitivity problem.

        The function is defined by the equation:

        g(x) = (Q/(Ks*B*sqrt((Zm-Zv)/L)))^(3.0/5.0)+Zv-Zb-Hd

        with:

        - Q : maximum annual flowrate (m3/s)
        - Ks : Strickler coefficient
        - Zv : downstream riverbed level (m)
        - Zm : upstream riverbed level (m)
        - L : Length of the river in meters
        - B : Width of the river in meters
        - Hd : height of the dyke (m)
        - Zb : the height of the bank (m)

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

        The model was first introduced in (Iooss, 2015).

        The analysis is the following.

        * The model has almost no interactions.
        * The most important variable is Q, with first order indice
          approximately equal to 0.4.
        * The variables L and B are insignificant.

        The reference Sobol' indices were computed from a sparse
        polynomial chaos.
        A Sobol' low discrepancy design of experiments was generated
        with 1000 training points.
        The sparse polynomial chaos expansion used an hyperbolic enumeration
        rule and a polynomial degree 8.
        The coefficients were estimated from regression.
        With 1000  points in the validation set, the Q2 was greater than 99.9%.
        There are 2 significant digits in the reference results.

        References
        ----------
        * Iooss, B., Lemaître, P.
          A review on global sensitivity analysis methods.
          In: Meloni, C., Dellino, G. (eds.) Uncertainty Management
          in Simulation-Optimization of Complex Systems.
          Algorithms and Applications. Springer, New York (2015)

        * "OpenTURNS: An industrial software for uncertainty quantification
          in simulation".
          Baudin, M., Dutfoy, A., Looss, B., Popelin, A.-L. 2017.
          Handbook of Uncertainty Quantification. pp. 2001-2038
        """

        formulas = ["(Q / (Ks * B * sqrt((Zm - Zv) / L)))^(3.0 / 5.0) + Zv - Zb - Hd"]
        function = ot.SymbolicFunction(
            ["Q", "Ks", "Zv", "Zm", "Hd", "Zb", "L", "B"], formulas
        )
        function.setOutputDescription(["S (m)"])

        # Define the distribution
        QGumbel = ot.Gumbel(558.0, 1013.0)
        Q = ot.TruncatedDistribution(QGumbel, 0, ot.TruncatedDistribution.LOWER)
        Q.setDescription(["Q (m3/s)"])
        KsNormal = ot.Normal(30.0, 7.5)
        Ks = ot.TruncatedDistribution(KsNormal, 0, ot.TruncatedDistribution.LOWER)
        Ks.setDescription(["Ks (m^(1/3)/s)"])
        Zv = ot.Uniform(49.0, 51.0)
        Zv.setDescription(["Zv (m)"])
        Zm = ot.Uniform(54.0, 56.0)
        Zm.setDescription(["Zm (m)"])
        #
        Hd = ot.Uniform(7.0, 9.0)  # Hd = 3.0;
        Hd.setDescription(["Hd (m)"])
        Zb = ot.Triangular(55.0, 55.5, 56.0)  # Zb = 55.5
        Zb.setDescription(["Zb (m)"])
        L = ot.Triangular(4990, 5000.0, 5010.0)  # L = 5.0e3;
        L.setDescription(["L (m)"])
        B = ot.Triangular(295.0, 300.0, 305.0)  # B = 300.0
        B.setDescription(["B (m)"])

        distribution = ot.ComposedDistribution((Q, Ks, Zv, Zm, Hd, Zb, L, B))

        name = "Flooding"

        # Compute exact indices
        firstOrderIndices = ot.Point([0.38, 0.13, 0.25, 0.00, 0.19, 0.02, 0.00, 0.00])
        totalOrderIndices = ot.Point([0.40, 0.15, 0.25, 0.01, 0.19, 0.02, 0.00, 0.00])

        super(FloodingSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None
