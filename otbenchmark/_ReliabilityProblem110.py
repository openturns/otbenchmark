"""
Created on Thu Apr 23 11:05:38 2020

@author: Jebroun

Class to define the ReliabilityProblem110 benchmark problem.
"""

from ._ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem110(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, mu=[0.0] * 2, sigma=[1.0] * 2):
        r"""
        Creates a reliability problem RP110.

        The event is :math:`\{g(\boldsymbol{X}) < \text{threshold}\}` where:

        .. math::
            g(\boldsymbol{x}) = \min(g_1(\boldsymbol{x}), g_2(\boldsymbol{x}))

        for any :math:`\boldsymbol{x} \in \mathbb{R}^2` with :

        .. math::
            g_1(\boldsymbol{x}) =
            \begin{cases}
            0.85 - 0.1 x_1 & \text{ if } x_1 \leq 3.5, \\
            4 - x_1 & \text{otherwise,}
            \end{cases}

        and:

        .. math::
            g_2(\boldsymbol{x}) =
            \begin{cases}
            2.3 - x_2  & \text{ if }  x_2 \leq 2, \\
            0.5 - 0.1 x_2 & \text{otherwise,}
            \end{cases}

        We have:

        * :math:`X_1 \sim \mathcal{N}(\mu_1, \sigma_1^2)` and
        * :math:`X_2 \sim \mathcal{N}(\mu_2, \sigma_2^2)`.

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
        equations = [
            "var g1 := (x0 <= 3.5) ? 0.85 - 0.1 * x0 : 4 - x0;",
            "var g2 := (x1 <= 2.0) ? 2.3 - x1 : 0.5 - 0.1 * x1;",
            "gsys := min(g1, g2);",
        ]
        program = "\n".join(equations)
        limitStateFunction = ot.SymbolicFunction(["x0", "x1"], ["gsys"], program)
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

        myDistribution = ot.JointDistribution([X1, X2])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP110"
        probability = 0.0000319
        super(ReliabilityProblem110, self).__init__(name, thresholdEvent, probability)
        return None
