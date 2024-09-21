#!/usr/bin/python
# coding:utf-8
# Copyright 2020 - 2021 EDF
"""Class to define a Oscillator sensitivity benchmark problem."""

from ._SensitivityBenchmarkProblem import SensitivityBenchmarkProblem
import openturns as ot
import numpy as np


class NLOscillatorSensitivity(SensitivityBenchmarkProblem):
    """Class to define a Oscillator sensitivity benchmark problem."""

    def __init__(self):
        """
        Create a nonlinear oscillator sensitivity problem.

        The function is defined by the equation:

        .. math::
            g(x) = fs - 3*ks*np.sqrt(np.pi*S0/(4.*xis*omegas**3)*
                xi_a*xis/(xip*xis*(4.*xi_a**2+theta**2)+gamma*xi_a**2)*
                (xip*omegap**3+xis*omegas**3)*omegap/(4.*xi_a*omegaa**4))

        where
        * omegap = np.sqrt(kp/mp)
        * omegas = np.sqrt(ks/ms)
        * omegaa = 0.5*(omegap+omegas)
        * gamma = ms/mp
        * xi_a = 0.5*(xip+xis)
        * theta = 1./omegaa*(omegap-omegas)

        The input random variables are independent.

        The aim is to assess reliability of a two-degree-of-freedom
        primary-secondary system under a white noise base acceleration.

        The basic variables characterizing the physical behavior are
        * the masses mp and ms
        * spring stiffnesses kp and ks
        * natural frequencies ωp and ωs
        * damping ratios ξp and ξs

        where the subscripts p and s respectively refer to
        the primary and secondary oscillators.

        The variables in the model are:
        * Fs : the force capacity of the secondary spring,
        * S0 is the intensity of the white noise,
        * ωp=(kp/mp)1/2,
        * ωs=(ks/ms)1/2,
        * ωa=(ωp+ωs)/2 the average frequency ratio,
        * γ=ms/mp the mass ratio,
        * ξa=(ξp+ξs)/2 the average damping ratio and
        * r=(ωp−ωs)/ωa a tuning parameter.

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

        The two interesting characteristics of this application test-case
        are its set of non-normal basic random variables and the fact that
        it suffers from a highly nonlinear limit-state surface (which
        prevents from using any FORM-based approach). Moreover, following,
        it seems relevant to consider the mean of the force capacity Fs as
        the most influent distribution parameter on the failure probability.

        The analysis is the following.

        * The most influential parameter is Fs with first order indice
          equal to 0.4.
          It has no interaction with other variables.

        * The second most influential parameter is kp, with
          first order indice equal to 0.18.
          It has small interactions with other parameters, since
          its total order indice is equal to 0.23.

        * The variable S0 is insignificant.

        References
        ----------
        * A. Der Kiureghian, M. De Stefano, Efficient algorithm for
          second-order reliability analysis, J. Eng. Mech. 117 (12) (1991) 2904–2923.

        * J.-M. Bourinet, F. Deheeger, M. Lemaire, Assessing small
          failure probabilities by combined subset simulation and
          Support Vector Machines, Struct. Saf. 33 (6) (2011) 343–353.

        * J.-M. Bourinet, Rare-event probability estimation with adaptive
          support vector regression surrogates,
          Reliab. Eng. Syst. Saf. 150 (2016) 210–221.

        * V. Dubourg, Adaptive surrogate models for reliability analysis
          and reliability-based design optimization, PhD thesis,
          Université Blaise Pascal – Clermont II, 2011.

        * Vincent Chabridon, Mathieu Balesdent, Jean-Marc Bourinet,
          Jérôme Morio, Nicolas Gayton.
          Evaluation of failure probability under parameter epistemic
          uncertainty: application to aerospace system reliability assessment.
          Aerospace Science and Technology, Elsevier, 2017, 69, pp.526-537.

        * Analyse de sensibilité fiabiliste avec prise en compte
          d’incertitudes sur le modèle probabiliste,
          Thèse présentée par Vincent Chabridon, 2019.

        """

        def oscillator(x):
            fs, mp, ms, kp, ks, xip, xis, S0 = x
            omegap = np.sqrt(kp / mp)
            omegas = np.sqrt(ks / ms)
            omegaa = 0.5 * (omegap + omegas)
            gamma = ms / mp
            xi_a = 0.5 * (xip + xis)
            theta = 1.0 / omegaa * (omegap - omegas)
            t1 = np.pi * S0 / (4.0 * xis * omegas**3)
            t2 = xi_a * xis / (xip * xis * (4.0 * xi_a**2 + theta**2) + gamma * xi_a**2)
            t3 = (xip * omegap**3 + xis * omegas**3) * omegap / (4.0 * xi_a * omegaa**4)
            F = fs - 3.0 * ks * np.sqrt(t1 * t2 * t3)
            return [F]

        dimension = 8
        function = ot.PythonFunction(dimension, 1, oscillator)

        mean_list = [21.5, 1.5, 0.01, 1.0, 0.01, 0.05, 0.02, 100.0]
        cov_list = [0.1, 0.1, 0.1, 0.2, 0.2, 0.4, 0.5, 0.1]
        description = ["fs", "mp", "ms", "kp", "ks", "xip", "xis", "S0"]
        myCollection = ot.DistributionCollection(dimension)
        for i, (mu, cov) in enumerate(zip(mean_list, cov_list)):
            myParam = ot.LogNormalMuSigma(mu, mu * cov, 0.0)
            marginal_distribution = ot.ParametrizedDistribution(myParam)
            marginal_distribution.setDescription([description[i]])
            myCollection[i] = marginal_distribution

        distribution = ot.ComposedDistribution(myCollection)

        name = "N.L. Oscillator"

        # Compute exact indices
        firstOrderIndices = ot.Point([0.40, 0.03, 0.09, 0.18, 0.12, 0.05, 0.05, 0.00])
        totalOrderIndices = ot.Point([0.40, 0.04, 0.10, 0.23, 0.16, 0.07, 0.06, 0.01])

        super(NLOscillatorSensitivity, self).__init__(
            name, distribution, function, firstOrderIndices, totalOrderIndices
        )

        return None
