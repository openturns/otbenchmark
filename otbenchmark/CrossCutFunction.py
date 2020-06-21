#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a drawable cross-cut function.
"""
import openturns as ot
import pylab as pl
import openturns.viewer as otv


class CrossCutFunction:
    """Create a drawable cross-cut function."""

    def __init__(self, function, referencePoint):
        """
        Create a drawable cross-cut function.

        Parameters
        ----------
        refencePoint : ot.Point
            The reference point of the function.
        """
        self.function = function
        self.referencePoint = referencePoint

    def draw(self, interval, numberOfPoints=[50] * 2):
        """
        Draw cross-cuts of the function in the bounds.

        Parameters
        ----------
        interval : ot.Interval
            The bounds where the function must be plotted.
        numberOfPoints : list of 2 ints
            The number of points in the X and Y axes.

        Returns
        -------
        fig : Matplotlib.figure
            The grid of cross-cuts plots.
        """
        inputDimension = self.function.getInputDimension()
        lowerBound = interval.getLowerBound()
        upperBound = interval.getUpperBound()
        fig = pl.figure(figsize=(12, 12))
        for i in range(inputDimension):
            # Diagonal part :
            # y(xi) where x(j != i) is equal to the reference
            # Create the cross cut function
            crossCutIndices = []
            crossCutReferencePoint = []
            for k in range(inputDimension):
                if k != i:
                    crossCutIndices.append(k)
                    crossCutReferencePoint.append(self.referencePoint[k])
            crossCutFunction = ot.ParametricFunction(
                self.function, crossCutIndices, crossCutReferencePoint
            )
            # Create bounds
            crossCutLowerBound = [lowerBound[i]]
            crossCutUpperBound = [upperBound[i]]
            # Draw
            graph = crossCutFunction.draw(
                crossCutLowerBound, crossCutUpperBound, numberOfPoints
            )
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
                        crossCutReferencePoint.append(self.referencePoint[k])
                crossCutFunction = ot.ParametricFunction(
                    self.function, crossCutIndices, crossCutReferencePoint
                )
                # Create bounds
                crossCutLowerBound = [lowerBound[i], lowerBound[j]]
                crossCutUpperBound = [upperBound[i], upperBound[j]]
                # Draw
                graph = crossCutFunction.draw(
                    crossCutLowerBound, crossCutUpperBound, numberOfPoints
                )
                # Remove unnecessary labels
                if i < inputDimension - 1:
                    graph.setXTitle("")
                graph.setTitle("Iso-values of limit state function")
                index = 1 + i * inputDimension + j
                ax = fig.add_subplot(inputDimension, inputDimension, index)
                _ = otv.View(graph, figure=fig, axes=[ax])
        _ = fig.suptitle("Cross-cuts of function")
        return fig
