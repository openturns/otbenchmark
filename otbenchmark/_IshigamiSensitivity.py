# Copyright 2020 EDF
"""Class to define a Ishigami sensitivity benchmark problem."""

from ._SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot
import numpy as np


class IshigamiSensitivity(SensitivityBenchmarkProblem):
    """Class to define a Ishigami sensitivity benchmark problem."""

    @staticmethod
    def ComputeIndices(a, b):
        """
        Compute the exact Sobol' indices of the Ishigami test case.

        Parameters
        ----------
        a : float
            The first parameter.
        b : float
            The second parameter.

        Returns
        -------
        exact : dict
            The exact expectation, variance, first order Sobol' indices,
            total order Sobol' indices.

        """
        var = 1.0 / 2 + a**2 / 8 + b * np.pi**4 / 5 + b**2 * np.pi**8 / 18
        S1 = (1.0 / 2 + b * np.pi**4 / 5 + b**2 * np.pi**8 / 50) / var
        S2 = (a**2 / 8) / var
        S3 = 0
        S13 = b**2 * np.pi**8 / 2 * (1.0 / 9 - 1.0 / 25) / var
        exact = {
            "expectation": a / 2,
            "variance": var,
            "S1": (1.0 / 2 + b * np.pi**4 / 5 + b**2 * np.pi**8.0 / 50) / var,
            "S2": (a**2 / 8) / var,
            "S3": 0,
            "S12": 0,
            "S23": 0,
            "S13": S13,
            "S123": 0,
            "T1": S1 + S13,
            "T2": S2,
            "T3": S3 + S13,
        }
        return exact

    def __init__(self, a=7.0, b=0.1):
        r"""
        Create a Ishigami sensitivity problem.

        The function is defined by the equation:

        .. math::
            g(\boldsymbol{x}) = \sin(x_1) + a \, \sin^2(x_2) + b \, x_3^4 \, \sin(x_1)

        for any :math:`\boldsymbol{x} \in [-\pi, \pi]^3`, where :math:`a, b` are parameters.
        We assume that :math:`X_1, X_2, X_3 \sim \mathcal{U}([- \pi, \pi])`.
        The input random variables are independent.

        Parameters
        ----------
        a : float
            The first parameter.

        b : float
            The second parameter.

        Examples
        --------
        >>> import otbenchmark as otb
        >>> problem = otb.IshigamiSensitivity()

        Notes
        -----
        The dimension of this problem cannot be changed, but
        its parameters can.
        The Sobol' sensitivity indices are computed from the values
        of the parameters.

        The distribution of the output of the Ishigami function has two modes.

        The expectation and the variance of :math:`Y` are

        .. math::
            \Expect{Y}  = \frac{a}{2}


        and:

        .. math::
            \Var{Y} = \frac{1}{2} +  \frac{a^2}{8} +  \frac{b^2 \pi^8}{18} +  \frac{b\pi^4}{5}.


        The Sobol' decomposition variances are

        .. math::
            V_1     = \frac{1}{2} \left(1 + b\frac{\pi^4}{5} \right)^2, \qquad
            V_2     = \frac{a^2}{8}, \qquad
            V_{1,3} = b^2 \pi^8 \frac{8}{225}


        and :math:`V_3=V_{1,2} = V_{2,3}=V_{1,2,3} = 0`.

        This leads to the following first order Sobol' indices:

        .. math::
            S_1 = \frac{V_1}{\Var{Y}}, \qquad S_2 = \frac{V_2}{\Var{Y}}, \qquad
            S_3 = 0,

        and the following total order indices:

        .. math::
            ST_1 = \frac{V_1+V_{1,3}}{\Var{Y}}, \qquad ST_2 = S_2, \qquad
            ST_3 = \frac{V_{1,3}}{\Var{Y}}.

        The first order indice of :math:`X_3` is equal to zero and the total order
        indice of :math:`X_3` is strictly positive: the variable :math:`X_3` has an influence on the
        output only through its interaction with :math:`X_1`.

        The detailed analysis is the following:

        * The variable :math:`X_1` has a total indice close to 0.6 has the
          highest impact on the output variability, by :math:`X_1` on its own or
          by its interactions with other variables.
          Indeed, its first order indice is close to 0.3, which
          implies that interactions of :math:`X_1` with other variables are involved
          in 0.6 - 0.3 = 0.3 of the variability of the output.
        * The variable :math:`X_2` has a first order indice approximately equal to 0.4,
          which is close to the total order indice.
          This shows that this variable does not interact with other variables.
        * The variable :math:`X_3` has a first order indice equal to zero.
          Since its total order indice is approximately equal to 0.3,
          this shows that its impact on the output is only through its
          interaction with :math:`X_1`.

        The function was first introduced in (Ishigami & Homma, 1990).

        References
        ----------
        * Ishigami, T., & Homma, T. (1990, December).
          An importance quantification technique in uncertainty analysis
          for computer models.
          In Uncertainty Modeling and Analysis, 1990. Proceedings.,
          First International Symposium on (pp. 398-403). IEEE.

        * Sobol', I. M., & Levitan, Y. L. (1999).
          On the use of variance reducing multipliers in Monte Carlo
          computations of a global sensitivity index.
          Computer Physics Communications, 117(1), 52-61.

        * "Sensitivity analysis in practice", Saltelli, Tarantolla,
          Compolongo, Ratto, Wiley, 2004

        """

        # Define the function
        formula = ["sin(X1) + a * sin(X2)^2 + b * X3^4 * sin(X1)"]
        input_names = ["X1", "X2", "X3", "a", "b"]
        fullFunction = ot.SymbolicFunction(input_names, formula)
        indices = [3, 4]
        referencePoint = [a, b]
        function = ot.ParametricFunction(fullFunction, indices, referencePoint)

        # Define the distribution
        inputDimension = 3
        distributionList = [ot.Uniform(-np.pi, np.pi)] * inputDimension
        distribution = ot.JointDistribution(distributionList)

        name = "Ishigami"

        # Compute exact indices
        exact = self.ComputeIndices(a, b)
        firstOrderIndices = ot.Point([exact["S1"], exact["S2"], exact["S3"]])
        totalOrderIndices = ot.Point([exact["T1"], exact["T2"], exact["T3"]])

        super(IshigamiSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None
