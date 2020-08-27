#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 17:23:25 2020

@author: osboxes
"""

import openturns as ot
import pylab as pl
import openturns.viewer as otv
import otbenchmark as otb


class CrossCutDistribution:
    """A distribution with cross-cut drawable features."""

    def __init__(self, distribution):
        """
        Create a distribution with cross-cut drawable features.

        Parameters
        ----------
        distribution : ot.Distribution
            A distribution.
        """
        self.distribution = distribution

    def drawConditionalPDF(self, referencePoint):
        """
        Draw the PDF of the conditional distribution.

        Within the grid, duplicate X and Y axes labels are removed, so that
        the minimum amount of labels are printed, reducing the risk of overlap.

        Each i-th graphics of the diagonal of the plot present the
        conditional distribution:
        X | Xi=referencePoint[i].

        Each (i,j)-th graphics of the diagonal of the plot present the
        conditional distribution:
        X | Xi=referencePoint[i], Xi=referencePoint[j]
        for i different from j.

        Parameters
        ----------
        referencePoint : ot.Point
            The conditioning point value.
        """
        description = self.distribution.getDescription()
        inputDimension = self.distribution.getDimension()
        fig = pl.figure(figsize=(12, 12))
        _ = fig.suptitle("Iso-values of conditional PDF")
        for i in range(inputDimension):
            # Diagonal part :
            # PDF(xi) where x(j != i) is equal to the reference
            # Create the cross cut function
            crossCutIndices = []
            crossCutReferencePoint = []
            for k in range(inputDimension):
                if k != i:
                    crossCutIndices.append(k)
                    crossCutReferencePoint.append(referencePoint[k])
            conditionalDistribution = ot.Distribution(
                otb.ConditionalDistribution(
                    self.distribution, crossCutIndices, crossCutReferencePoint
                )
            )
            # Draw
            graph = conditionalDistribution.drawPDF()
            graph.setXTitle(description[i])
            graph.setLegends([""])
            index = 1 + i * inputDimension + i
            ax = fig.add_subplot(inputDimension, inputDimension, index)
            _ = otv.View(graph, figure=fig, axes=[ax])
            # Lower triangle : y(xi, xj) where x(k != i and k != j)
            # is equal to the reference
            for j in range(i):
                # Draw the cross cut (Xi, Xj), where all other variables
                # are set to the reference value
                # Create the cross cut function
                crossCutIndices = []
                crossCutReferencePoint = []
                for k in range(inputDimension):
                    if k != i and k != j:
                        crossCutIndices.append(k)
                        crossCutReferencePoint.append(referencePoint[k])
                conditionalDistribution = ot.Distribution(
                    otb.ConditionalDistribution(
                        self.distribution, crossCutIndices, crossCutReferencePoint
                    )
                )
                # Draw
                graph = conditionalDistribution.drawPDF()
                # Workaround for https://github.com/openturns/openturns/issues/1230
                # The ConditionalDistribution should manage the description, but
                # cannot because of a limitation in OT.
                # Explanation: j is the column number in the plot grid
                graph.setXTitle(description[j])
                # Explanation: i is the row number in the plot grid
                graph.setYTitle(description[i])
                print("Descr = ", i, j)
                # Remove unnecessary labels
                # Only the last bottom i-th row has a X axis title
                if i < inputDimension - 1:
                    graph.setXTitle("")
                # Only the first left column has a Y axis title
                if j > 0:
                    graph.setYTitle("")
                graph.setTitle("Iso-values of conditional PDF")
                index = 1 + i * inputDimension + j
                ax = fig.add_subplot(inputDimension, inputDimension, index)
                _ = otv.View(graph, figure=fig, axes=[ax])
        return fig

    def drawMarginalPDF(self):
        """
        Draw the PDF of the marginal distribution.

        Within the grid, duplicate X and Y axes labels are removed, so that
        the minimum amount of labels are printed, reducing the risk of overlap.

        Each i-th graphics of the diagonal of the plot present the
        marginal i-th distribution X[i].

        Each (i,j)-th graphics of the diagonal of the plot present the
        marginal distribution (X[i], X[j]) for i different from j.
        """
        inputDimension = self.distribution.getDimension()
        fig = pl.figure(figsize=(12, 12))
        _ = fig.suptitle("Iso-values of marginal PDF")
        for i in range(inputDimension):
            # Diagonal part :
            marginalDistribution = self.distribution.getMarginal([i])
            # Draw
            graph = marginalDistribution.drawPDF()
            graph.setLegends([""])
            index = 1 + i * inputDimension + i
            ax = fig.add_subplot(inputDimension, inputDimension, index)
            _ = otv.View(graph, figure=fig, axes=[ax])
            # Lower triangle : y(xi, xj) where x(k != i and k != j)
            # is equal to the reference
            for j in range(i):
                # We want X[j] on X-axis and X[i] on Y-axis
                marginalDistribution = self.distribution.getMarginal([j, i])
                graph = marginalDistribution.drawPDF()
                # Remove unnecessary labels
                # Only the last bottom i-th row has a X axis title
                if i < inputDimension - 1:
                    graph.setXTitle("")
                # Only the first left column has a Y axis title
                if j > 0:
                    graph.setYTitle("")
                graph.setTitle("Iso-values of marginal PDF")
                index = 1 + i * inputDimension + j
                ax = fig.add_subplot(inputDimension, inputDimension, index)
                _ = otv.View(graph, figure=fig, axes=[ax])
        return fig
