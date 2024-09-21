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
        useIntegration=True,
        sampleSizeForCDFBySampling=10000,
        verbose=False,
    ):
        """
        Create a conditional distribution.

        This is the random variable:

        Y = (X | X[i]=conditionalRefencePoint[i])

        for i in conditionalIndices.

        The dimension of Y is the dimension of X minus the number
        of conditioned indices:

        dimension(Y) = dimension(X) - len(conditionalIndices)

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
        useIntegration : bool
            Set to True to use integration, False to use sampling.
            Default is True.
        sampleSizeForCDFBySampling : int
            The sample size used for sampling. The default is 10000.
        verbose : bool
            Set to True to print intermediate messages.
            Default is False.

        Examples
        --------
        # The random variable is (X0, X1, X2)
        >>> import openturns as ot
        >>> import otbenchmark as otb
        >>> distribution = ot.Normal(3)
        # We condition X = (X0, X1, X2) given X1=2.0, X2=3.0
        >>> conditionalIndices = [1, 2]
        >>> conditionalRefencePoint = [2.0, 3.0]
        >>> conditionalDistribution = ot.Distribution(otb.ConditionalDistribution(
        ...     distribution, conditionalIndices, conditionalRefencePoint))
        # PDF
        >>>  computed = conditionalDistribution.computePDF([1.0])
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
        self.verbose = verbose
        self.useIntegration = useIntegration
        self.sampleSizeForCDFBySampling = sampleSizeForCDFBySampling
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
        # Compute unconditioned indices
        dimension = self.distribution.getDimension()
        self.unconditionedIndices = []
        for i in range(dimension):
            if i not in self.conditionalIndices:
                self.unconditionedIndices.append(i)
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

    def computeCDF(self, Y):
        """
        Returns the CDF.

        Parameters
        ----------
        Y : ot.Point(dimension_Y)
            The input point.

        Returns
        -------
        p : float
            The CDF of the conditional distribution.
        """
        if self.verbose:
            print("computeCDF at", Y)

        if self.useIntegration:
            p = self._compute_CDF_by_integration(Y)
        else:
            p = self._compute_CDF_by_sampling(Y)
        return p

    def _compute_CDF_by_integration(self, Y):
        """
        Compute the value of the CDF at point Y.

        Parameters
        ----------
        Y : ot.Point(dimension_Y)
            The point where the CDF must be evaluated.

        Returns
        -------
        p : float, in [0, 1]
            The value of the CDF.

        """

        def DistributionPDFIntegrand(Y):
            X = self.computeExtendedInput(Y)
            pdf = self.distribution.computePDF(X)
            return [pdf]

        distributionPDFIntegrandPy = ot.PythonFunction(
            self.conditionalDimension, 1, DistributionPDFIntegrand
        )
        # Bounds = (lowerBound, X)
        lowerBound = self.distributionRange.getLowerBound()
        integrationRange = ot.Interval(lowerBound, Y)
        value = self.quadrature.integrate(distributionPDFIntegrandPy, integrationRange)
        p = value[0] / self.integrationFactor
        p = min(1.0, max(0.0, p))
        return p

    def _compute_CDF_by_sampling(self, Y):
        """
        Compute the value of the CDF at point Y by sampling.

        Parameters
        ----------
        Y : ot.Point(dimension_Y)
            The point where to evaluate the CDF.

        Returns
        -------
        p : float, in [0, 1]
            The value of the CDF.

        """

        # Compute F_Y(X) where Y is the conditioned random vector.
        unconditionedDistribution = self.distribution.getMarginal(
            self.unconditionedIndices
        )

        # Create the domain from [-INF] up to Y.
        unconditioned_dimension = len(Y)
        lower_bound = [-ot.SpecFunc.MaxScalar] * unconditioned_dimension
        upper_bound = Y
        domain = ot.Interval(lower_bound, upper_bound)
        # Create a domain event
        unconditioned_random_vector = ot.RandomVector(unconditionedDistribution)
        event = ot.DomainEvent(unconditioned_random_vector, domain)
        event_sample = event.getSample(self.sampleSizeForCDFBySampling)
        p = event_sample.computeMean()[0]
        return p

    def computePDF(self, Y):
        """
        Returns the PDF.

        Returns
        -------
        y : float
            The PDF of the conditional distribution.
        """
        if self.verbose:
            print("computePDF at", Y)
        X = self.computeExtendedInput(Y)
        pdfConditioned = self.distribution.computePDF(X)
        pdf = pdfConditioned / self.integrationFactor
        return pdf

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

    def computeExtendedInput(self, Y):
        """
        Compute the extended input from the conditioned input.

        The conditioned input is Y.
        The function returns the vector

        X = (X[0], X[1], ..., X[dimension - 1])

        so that

        X[i] = X[i] if i is conditionned
        conditionalRefencePoint[i] otherwise,

        for i = 0, 1, ..., dimension - 1.

        The following algorithm implements this:

        .. code-block:: python

            X = []
            referenceIndex = 0
            conditionalIndex = 0
            for i in range(self.extendedDimension):
                if i in self.conditionalIndices:
                    X.append(self.conditionalRefencePoint[referenceIndex])
                    referenceIndex += 1
                else:
                    X.append(X[conditionalIndex])
                    conditionalIndex += 1

        The actual code is, however, vectorized using numpy.

        Parameters
        ----------
        Y : ot.Point
            The conditioned input point.
        extendedDimension : int
            The extended dimension.
        conditionalIndices : list
            The indices of the marginal which are conditioned
        conditionalRefencePoint : list
            The values of the marginal which are conditioned

        Returns
        -------
        X : ot.Point
            The extended input point, as an input of the full distribution.
        """
        if self.verbose:
            Y = ot.Point(Y)
            print("computeExtendedInput, Y =", Y)
        X = np.zeros(self.extendedDimension)
        X[self.conditionalIndices] = self.conditionalRefencePoint
        X[~self.mask] = Y
        X = ot.Point(X)
        if self.verbose:
            print("X=", X)
        return X
