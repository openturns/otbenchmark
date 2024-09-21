"""
Estimates Sobol' indices with Janon estimator.

Alexandre Janon, Thierry Klein, Agnes Lagnoux-Renaudie, Maëlle Nodet,
Clémentine Prieur.
Asymptotic normality and efficiency of two Sobol index estimators.
ESAIM: Probability and Statistics, EDP Sciences, 2014, 18, pp.342-364.
⟨10.1051/ps/2013040⟩. ⟨hal-00665048v2⟩

Notice that the denominator of equation 8 page 4 of the paper published in HAL
is wrong.
It has been corrected in the equation 2.8 page 345 of the paper published in ESAIM
(the squares were moved into the equation).
"""

import openturns as ot
import numpy as np


def computeSumDotSamples(sampleX, sampleY):
    """
    Compute the product and sum of the components of two samples.

    This is:

    .. math::
        S = sum_{i = 1}^n x_i * y_i

    Parameters
    ----------
    sampleX : ot.Sample(size, dimension)
        The first sample.
    sampleY : ot.Sample(size, dimension)
        The first sample.

    Returns
    -------
    value : float
        The result.

    """
    # Multiplication and sum of two Samples
    value = np.sum(np.array(sampleX) * np.array(sampleY))
    return value


class JanonSensitivityAlgorithm(ot.SobolIndicesAlgorithm):
    def __init__(self, inputDesign, outputDesign, size):
        """
        Estimates Sobol' indices with Janon estimator.

        This estimator only implements an output dimension equal to 1.

        Parameters
        ----------
        inputDesign : ot.Sample(size, dimension)
            The input sample.
        outputDesign : ot.Sample(required_size, dimension)
            The output sample.
        size : int
            The basic size of the sample.

        Returns
        -------
        None.

        """
        self.inputDesign = inputDesign
        self.inputDimension = inputDesign.getDimension()
        self.outputDimension = outputDesign.getDimension()
        self.size = size
        self.outputDesign = outputDesign
        self.indicesF = ot.Point(self.inputDimension)
        self.indicesT = ot.Point(self.inputDimension)

        # Compute muA = mean(yA)
        yA = ot.Sample(outputDesign, 0, size)
        muA = yA.computeMean()

        # Compute muB
        yB = ot.Sample(outputDesign, size, 2 * size)
        muB = yB.computeMean()

        for p in range(self.inputDimension):
            # yE correspond to the block that start at index (p + 2) * size
            yE = ot.Sample(outputDesign, (2 + p) * self.size, (3 + p) * self.size)
            muE = yE.computeMean()
            # For first order indices, consider yE and yB
            muEB = (muE + muB) / 2.0
            yE_centered = yE - muEB
            yB_centered = yB - muEB
            numerator = computeSumDotSamples(yE_centered, yB_centered)
            y_squared = (np.array(yE) ** 2 + np.array(yB) ** 2) / 2.0 - muEB[0] ** 2
            denominator = np.sum(y_squared)
            self.indicesF[p] = numerator / denominator
            # For total order indices, consider yE and yA
            muEA = (muE + muA) / 2.0
            yE_centered = yE - muEA
            yA_centered = yA - muEA
            numerator = computeSumDotSamples(yE_centered, yA_centered)
            y_squared = (np.array(yE) ** 2 + np.array(yA) ** 2) / 2.0 - muEA[0] ** 2
            denominator = np.sum(y_squared)
            self.indicesT[p] = 1.0 - numerator / denominator

    def getFirstOrderIndices(self):
        """
        Returns first order Sobol' indices.

        Returns
        -------
        indices : ot.Point(dimension)
            The first order Sobol' indices.

        """
        return self.indicesF

    def getTotalOrderIndices(self):
        """
        Returns total order Sobol' indices.

        Returns
        -------
        indices : ot.Point(dimension)
            The total order Sobol' indices.

        """
        return self.indicesT
