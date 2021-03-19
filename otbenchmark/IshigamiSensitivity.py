#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define a Ishigami sensitivity benchmark problem."""

from otbenchmark.SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
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
        var = 1.0 / 2 + a ** 2 / 8 + b * np.pi ** 4 / 5 + b ** 2 * np.pi ** 8 / 18
        S1 = (1.0 / 2 + b * np.pi ** 4 / 5 + b ** 2 * np.pi ** 8 / 50) / var
        S2 = (a ** 2 / 8) / var
        S3 = 0
        S13 = b ** 2 * np.pi ** 8 / 2 * (1.0 / 9 - 1.0 / 25) / var
        exact = {
            "expectation": a / 2,
            "variance": var,
            "S1": (1.0 / 2 + b * np.pi ** 4 / 5 + b ** 2 * np.pi ** 8.0 / 50) / var,
            "S2": (a ** 2 / 8) / var,
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
        """
        Create a Ishigami sensitivity problem.

        The function is defined by the equation:

        g(x) = sin(X1) + a * sin(X2)^2 + b * X3^4 * sin(X1)

        where X1, X2, X3 in [-pi, pi].

        The distribution of the output of the Ishigami function has two modes.

        The first order indice of X3 is equal to zero and the total order
        indice of X3 is strictly posititive: this variable has an influence on the
        output only through its interaction with X1.

        References
        ----------
        * "Sensitivity analysis in practice", Saltelli, Tarantolla,
          Compolongo, Ratto, Wiley, 2004
        * "An importance quantification technique in uncertainty analysis for
          computer models", Ishigami, Homma, 1990, Proceedings of the ISUMA'90.
          First international symposium on uncertainty modelling and Analysis,
          University of Maryland, USA, pp. 398-403.

        Parameters
        ----------
        a : float
            The first parameter.

        b : float
            The second parameter.

        Example
        -------
        problem  = IshigamiSensitivity()
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
        distribution = ot.ComposedDistribution(distributionList)

        name = "Ishigami"

        # Compute exact indices
        exact = self.ComputeIndices(a, b)
        firstOrderIndices = ot.Point([exact["S1"], exact["S2"], exact["S3"]])
        totalOrderIndices = ot.Point([exact["T1"], exact["T2"], exact["T3"]])

        super(IshigamiSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None
