# Copyright 2020 EDF.
"""
Test for DrawEvent class.
"""
import openturns as ot
import otbenchmark
import unittest
import numpy as np


class CheckDrawEvent(unittest.TestCase):
    def test_DrawLimitState(self):
        # Distribution
        R = ot.Normal(4.0, 1.0)
        R.setDescription("R")
        S = ot.Normal(2.0, 1.0)
        S.setDescription("S")
        g = ot.SymbolicFunction(["R", "S"], ["R-S"])
        # Event
        distribution = ot.ComposedDistribution([R, S])
        inputRV = ot.RandomVector(distribution)
        outputRV = ot.CompositeRandomVector(g, inputRV)
        eventF = ot.ThresholdEvent(outputRV, ot.GreaterOrEqual(), 0.0)
        alpha = 1.0 - 1.0e-2
        (
            bounds,
            marginalProb,
        ) = distribution.computeMinimumVolumeIntervalWithMarginalProbability(alpha)
        drawEvent = otbenchmark.DrawEvent(eventF)
        _ = drawEvent.drawLimitStateCrossCut(bounds, 0, 1)
        # Avoid failing on CircleCi
        # _tkinter.TclError: no display name and no $DISPLAY environment variable
        try:
            _ = drawEvent.drawLimitState(bounds)
        except Exception as e:
            print(e)

    def test_DrawSample(self):
        # Distribution
        R = ot.Normal(4.0, 1.0)
        R.setDescription("R")
        S = ot.Normal(2.0, 1.0)
        S.setDescription("S")
        g = ot.SymbolicFunction(["R", "S"], ["R - S"])
        # Event
        distribution = ot.ComposedDistribution([R, S])
        inputRV = ot.RandomVector(distribution)
        outputRV = ot.CompositeRandomVector(g, inputRV)
        eventF = ot.ThresholdEvent(outputRV, ot.GreaterOrEqual(), 0)
        #
        sampleSize = 500
        drawEvent = otbenchmark.DrawEvent(eventF)
        _ = drawEvent.drawSampleCrossCut(sampleSize, 0, 1)
        # Avoid failing on CircleCi
        # _tkinter.TclError: no display name and no $DISPLAY environment variable
        try:
            _ = drawEvent.drawSample(sampleSize)
        except Exception as e:
            print(e)

    def test_DrawFilledEvent(self):
        # Distribution
        R = ot.Normal(4.0, 1.0)
        R.setDescription("R")
        S = ot.Normal(2.0, 1.0)
        S.setDescription("S")
        g = ot.SymbolicFunction(["R", "S"], ["R - S"])
        # Event
        distribution = ot.ComposedDistribution([R, S])
        inputRV = ot.RandomVector(distribution)
        outputRV = ot.CompositeRandomVector(g, inputRV)
        eventF = ot.ThresholdEvent(outputRV, ot.GreaterOrEqual(), 0)
        alpha = 1.0 - 1.0e-2
        (
            bounds,
            marginalProb,
        ) = distribution.computeMinimumVolumeIntervalWithMarginalProbability(alpha)
        #
        drawEvent = otbenchmark.DrawEvent(eventF)
        # Avoid failing on CircleCi
        # _tkinter.TclError: no display name and no $DISPLAY environment variable
        try:
            _ = drawEvent.fillEvent(bounds)
        except Exception as e:
            print(e)

    def test_DrawLimitStateMultidimensional(self):
        problem = otbenchmark.ReliabilityProblem33()
        event = problem.getEvent()
        inputVector = event.getAntecedent()
        distribution = inputVector.getDistribution()
        alpha = 1.0 - 1.0e-2
        (
            bounds,
            marginalProb,
        ) = distribution.computeMinimumVolumeIntervalWithMarginalProbability(alpha)
        # bounds
        drawEvent = otbenchmark.DrawEvent(event)
        # Avoid failing on CircleCi
        # _tkinter.TclError: no display name and no $DISPLAY environment variable
        try:
            _ = drawEvent.drawLimitState(bounds)
        except Exception as e:
            print(e)

    def test_DrawSampleMultidimensional(self):
        problem = otbenchmark.ReliabilityProblem33()
        event = problem.getEvent()
        sampleSize = 500
        drawEvent = otbenchmark.DrawEvent(event)
        # Avoid failing on CircleCi
        # _tkinter.TclError: no display name and no $DISPLAY environment variable
        try:
            _ = drawEvent.drawSample(sampleSize)
        except Exception as e:
            print(e)

    def test_DrawFilledEventMultidimensional(self):
        problem = otbenchmark.ReliabilityProblem33()
        event = problem.getEvent()
        inputVector = event.getAntecedent()
        distribution = inputVector.getDistribution()
        alpha = 1.0 - 1.0e-2
        (
            bounds,
            marginalProb,
        ) = distribution.computeMinimumVolumeIntervalWithMarginalProbability(alpha)
        #
        drawEvent = otbenchmark.DrawEvent(event)
        # Avoid failing on CircleCi
        # _tkinter.TclError: no display name and no $DISPLAY environment variable
        try:
            _ = drawEvent.fillEvent(bounds)
        except Exception as e:
            print(e)

    def test_DrawMultidimensional(self):
        problem = otbenchmark.ReliabilityProblem33()
        event = problem.getEvent()
        inputVector = event.getAntecedent()
        distribution = inputVector.getDistribution()
        alpha = 1.0 - 1.0e-4
        (
            bounds,
            marginalProb,
        ) = distribution.computeMinimumVolumeIntervalWithMarginalProbability(alpha)
        #
        drawEvent = otbenchmark.DrawEvent(event)
        # Avoid failing on CircleCi
        # _tkinter.TclError: no display name and no $DISPLAY environment variable
        try:
            _ = drawEvent.draw(
                bounds, drawLimitState=True, drawSample=True, fillEvent=True
            )
        except Exception as e:
            print(e)

    def test_drawInputOutputSample(self):
        problem = otbenchmark.ReliabilityProblem22()
        event = problem.getEvent()
        g = event.getFunction()
        inputVector = event.getAntecedent()
        distribution = inputVector.getDistribution()
        (
            bounds,
            marginalProb,
        ) = distribution.computeMinimumVolumeIntervalWithMarginalProbability(
            1.0 - 1.0e-6
        )
        #
        drawEvent = otbenchmark.DrawEvent(event)
        sampleSize = 1000
        inputSample = distribution.getSample(sampleSize)
        outputSample = g(inputSample)
        _ = drawEvent.drawInputOutputSample(inputSample, outputSample)

    def test_RP8Function(self):
        problem = otbenchmark.ReliabilityProblem8()
        event = problem.getEvent()
        inputVector = event.getAntecedent()
        distribution = inputVector.getDistribution()
        referencePoint = distribution.getMean()
        drawEvent = otbenchmark.DrawEvent(event)
        i = 3
        j = 4
        gCC34 = drawEvent.buildCrossCutFunction(i, j)
        X = [referencePoint[i], referencePoint[j]]
        y1 = gCC34(X)
        print("X=", X, "y1=", y1)
        np.testing.assert_almost_equal(y1, [270.0])

    def test_RP8(self):
        problem = otbenchmark.ReliabilityProblem8()
        event = problem.getEvent()
        inputVector = event.getAntecedent()
        distribution = inputVector.getDistribution()
        (
            bounds,
            marginalProb,
        ) = distribution.computeMinimumVolumeIntervalWithMarginalProbability(
            1.0 - 1.0e-6
        )
        #
        drawEvent = otbenchmark.DrawEvent(event)
        # Avoid failing on CircleCi
        # _tkinter.TclError: no display name and no $DISPLAY environment variable
        try:
            _ = drawEvent.drawSample(500)
            _ = drawEvent.draw(bounds)
        except Exception as e:
            print(e)
        sampleSize = 500
        i = 3
        j = 4
        _ = drawEvent.drawSampleCrossCut(sampleSize, i, j)


if __name__ == "__main__":
    unittest.main()
