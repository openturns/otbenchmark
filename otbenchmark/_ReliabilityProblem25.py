"""
Created on Mon Apr 20 11:18:59 2020

@author: Jebroun

Class to define the ReliabilityProblem25 benchmark problem.
"""

from ._ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem25(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, mu=[0.0] * 2, sigma=[1.0] * 2):
        r"""
        Creates a reliability problem RP25.

        The event is :math:`\{g(\boldsymbol{X}) < \text{threshold}\}` where

        .. math::

            g(x_1, x_2) = \max(x_1^2 - 8 x_2 + 16, -16 x_1 + x_2 + 32)

        for any :math:`\boldsymbol{x} \in \mathbb{R}^2`.

        We have:

        * x1 ~ Normal(mu[0], sigma[0]) and
        * x2 ~ Normal(mu[1], sigma[1]).

        Parameters
        ----------
        threshold : float
            The threshold.
        mu : sequence of floats
            The list of two items representing the means of the gaussian distributions.
        sigma : float
            The list of two items representing the standard deviations of
            the gaussian distributions.
        """
        equations = ["var g1 := x1^2 -8 * x2 + 16"]
        equations.append("var g2 := -16 * x1 + x2 + 32")
        equations.append("gsys := max(g1, g2)")
        formula = ";".join(equations)
        limitStateFunction = ot.SymbolicFunction(["x1", "x2"], ["gsys"], formula)
        inputDimension = len(mu)
        if inputDimension != 2:
            raise Exception(
                "The dimension of mu is %d, but the expected dimension is 2."
                % (inputDimension)
            )

        inputDimension = len(sigma)
        if inputDimension != 2:
            raise Exception(
                "The dimension of sigma is %d, but the expected dimension is 2."
                % (inputDimension)
            )
        X1 = ot.Normal(mu[0], sigma[0])
        X1.setDescription(["X1"])
        X2 = ot.Normal(mu[1], sigma[1])
        X2.setDescription(["X2"])

        myDistribution = ot.ComposedDistribution([X1, X2])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP25"
        probability = 4.148566293759747e-05
        super(ReliabilityProblem25, self).__init__(name, thresholdEvent, probability)
        return None
