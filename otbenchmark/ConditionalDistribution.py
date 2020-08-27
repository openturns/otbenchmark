#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A class to create a conditional distribution.
"""

import openturns as ot
import numpy as np


class ConditionalDistribution(ot.PythonDistribution):
    """A class to create a conditional distribution."""

    @staticmethod
    def ComputeRange(distribution, conditionalIndices, conditionalRefencePoint):
        """
        Compute the range of the conditional distribution.

        Parameters
        ----------
        distribution : ot.Distribution
            The distribution to be conditioned.
        conditionalIndices : list
            The indices of the marginal which are conditioned
        conditionalRefencePoint : list
            The values of the marginal which are conditioned

        Returns
        -------
        conditionalRange : ot.Interval
            The range of the conditional distribution.
        """
        fullRange = distribution.getRange()
        lowerBound = fullRange.getLowerBound()
        upperBound = fullRange.getUpperBound()
        conditionalLowerBound = []
        conditionalUpperBound = []
        for i in range(distribution.getDimension()):
            if i not in conditionalIndices:
                conditionalLowerBound.append(lowerBound[i])
                conditionalUpperBound.append(upperBound[i])
        conditionalRange = ot.Interval(conditionalLowerBound, conditionalUpperBound)
        return conditionalRange

    def __init__(
        self,
        distribution,
        conditionalIndices,
        conditionalRefencePoint,
        maximumSubIntervals=10000,
        maximumError=1.0e-3,
    ):
        """
        Create a conditional distribution.

        This is the random variable:

        X | X[i]=conditionalRefencePoint[i]
        for i in conditionalIndices.

        Computing the CDF of the distribution requires a numerical integration.
        This is done with IteratedQuadrature based on the univariate GaussKronrod
        integration method.

        Parameters
        ----------
        distribution : ot.Distribution
            The distribution to be conditioned.
        conditionalIndices : list
            The indices of the marginals which are conditioned
        conditionalRefencePoint : list
            The values of the marginal which are conditioned
        maximumSubIntervals : int
            The maximal number of subdivisions of the univariate interval.
        maximumError : float
            The maximal error between Gauss and Kronrod approximations.

        Examples
        --------
        # The random variable is (X0, X1, X2)
        distribution = ot.Normal(3)
        # We condition X = (X0, X1, X2) given X1=2.0, X2=3.0
        conditionalIndices = [1, 2]
        conditionalRefencePoint = [2.0, 3.0]
        conditionalDistribution = ot.Distribution(
            otbenchmark.ConditionalDistribution(
                distribution, conditionalIndices, conditionalRefencePoint
            )
        )
        # PDF
        computed = conditionalDistribution.computePDF([1.0])
        """
        if len(conditionalIndices) != len(conditionalRefencePoint):
            raise ValueError(
                "The dimension of the indices is %d"
                "but the dimension of the reference point is %s"
                % (len(conditionalIndices), len(conditionalRefencePoint))
            )
        self.conditionalIndices = conditionalIndices
        self.conditionalRefencePoint = conditionalRefencePoint
        self.distribution = distribution
        self.extendedDimension = distribution.getDimension()
        self.conditionalDimension = distribution.getDimension() - len(
            conditionalIndices
        )
        self.distributionRange = ConditionalDistribution.ComputeRange(
            distribution, conditionalIndices, conditionalRefencePoint
        )
        # Compute integration factor
        rule = ot.GaussKronrodRule(ot.GaussKronrodRule.G11K23)
        univariateIntegration = ot.GaussKronrod(maximumSubIntervals, maximumError, rule)
        self.quadrature = ot.IteratedQuadrature(univariateIntegration)
        if len(self.conditionalIndices) == 0:
            self.integrationFactor = 1.0
        else:
            conditionedDistribution = self.distribution.getMarginal(
                self.conditionalIndices
            )
            self.integrationFactor = conditionedDistribution.computePDF(
                self.conditionalRefencePoint
            )
        # Create the mask for extending inputs
        self.mask = np.zeros(self.extendedDimension, dtype=bool)
        self.mask[self.conditionalIndices] = True
        super(ConditionalDistribution, self).__init__(self.conditionalDimension)

    def getRange(self):
        """
        Returns the range.

        Returns
        -------
        conditionalRange : ot.Interval
            The range of the conditional distribution.
        """
        return self.distributionRange

    def computeCDF(self, X):
        """
        Returns the CDF.

        Returns
        -------
        p : float
            The CDF of the conditional distribution.
        """

        def DistributionPDFIntegrand(X):
            extendedX = self.computeExtendedInput(X)
            y = self.distribution.computePDF(extendedX)
            return [y]

        distributionPDFIntegrandPy = ot.PythonFunction(
            self.conditionalDimension, 1, DistributionPDFIntegrand
        )
        # Bounds = (lowerBound, X)
        lowerBound = self.distributionRange.getLowerBound()
        integrationRange = ot.Interval(lowerBound, X)
        value = self.quadrature.integrate(distributionPDFIntegrandPy, integrationRange)
        p = value[0] / self.integrationFactor
        p = min(1.0, max(0.0, p))
        return p

    def computePDF(self, X):
        """
        Returns the PDF.

        Returns
        -------
        y : float
            The PDF of the conditional distribution.
        """
        extendedX = self.computeExtendedInput(X)
        pdfConditioned = self.distribution.computePDF(extendedX)
        y = pdfConditioned / self.integrationFactor
        return y

    def getDescription(self):
        """
        Returns the description.

        Returns
        -------
        description : ot.Description
            The description of the conditional distribution.
        """
        # Does not work, because of https://github.com/openturns/openturns/issues/1230
        description = []
        extendedDescription = self.distribution.getDescription()
        conditionalIndex = 0
        for i in range(self.distribution.getDimension()):
            if i not in self.conditionalIndices:
                description.append(extendedDescription[conditionalIndex])
                conditionalIndex += 1
        return ot.Description(description)

    def computeExtendedInput(self, X):
        """
        Compute the extended input from the conditioned input.

        Parameters
        ----------
        X : ot.Point
            The conditioned input point.
        extendedDimension : int
            The extended dimension.
        conditionalIndices : list
            The indices of the marginal which are conditioned
        conditionalRefencePoint : list
            The values of the marginal which are conditioned

        Returns
        -------
        extendedX : ot.Point
            The extended input point, as an input of the full distribution.
        """
        if False:
            extendedX = []
            referenceIndex = 0
            conditionalIndex = 0
            for i in range(self.extendedDimension):
                if i in self.conditionalIndices:
                    extendedX.append(self.conditionalRefencePoint[referenceIndex])
                    referenceIndex += 1
                else:
                    extendedX.append(X[conditionalIndex])
                    conditionalIndex += 1
        else:
            extendedX = np.zeros(self.extendedDimension)
            extendedX[self.conditionalIndices] = self.conditionalRefencePoint
            extendedX[~self.mask] = X
        return ot.Point(extendedX)
