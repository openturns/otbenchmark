# -*- coding: utf-8 -*-
# Copyright 2020 EDF.
"""
Test for DrawEvent class.
"""
import openturns as ot
import otbenchmark
import unittest
import openturns.viewer as otv


class CheckDrawEvent(unittest.TestCase):
    def test_DrawLimitState(self):
        # Distribution
        R = ot.Normal(4.0, 1.0)
        R.setDescription("R")
        S = ot.Normal(2.0, 1.0)
        S.setDescription("S")
        g = ot.SymbolicFunction(["R", "S"], ["R-S"])
        # Event
        inputvector = ot.ComposedDistribution([R, S])
        inputRV = ot.RandomVector(inputvector)
        outputRV = ot.CompositeRandomVector(g, inputRV)
        eventF = ot.Event(outputRV, ot.GreaterOrEqual(), 0)
        # Bounds
        alphaMin = 0.01
        alphaMax = 1 - alphaMin
        lowerBound = ot.Point(
            [R.computeQuantile(alphaMin)[0], S.computeQuantile(alphaMin)[0]]
        )
        upperBound = ot.Point(
            [R.computeQuantile(alphaMax)[0], S.computeQuantile(alphaMax)[0]]
        )
        bounds = ot.Interval(lowerBound, upperBound)
        #
        drawEvent = otbenchmark.DrawEvent(eventF)
        graph = drawEvent.drawLimitState(bounds)
        otv.View(graph)

    def test_DrawSample(self):
        # Distribution
        R = ot.Normal(4.0, 1.0)
        R.setDescription("R")
        S = ot.Normal(2.0, 1.0)
        S.setDescription("S")
        g = ot.SymbolicFunction(["R", "S"], ["R - S"])
        # Event
        inputvector = ot.ComposedDistribution([R, S])
        inputRV = ot.RandomVector(inputvector)
        outputRV = ot.CompositeRandomVector(g, inputRV)
        eventF = ot.Event(outputRV, ot.GreaterOrEqual(), 0)
        #
        sampleSize = 500
        inputSample = inputvector.getSample(sampleSize)
        outputSample = g(inputSample)
        #
        drawEvent = otbenchmark.DrawEvent(eventF)
        graph = drawEvent.drawSample(inputSample, outputSample)
        otv.View(graph)

    def test_DrawFilledEvent(self):
        # Distribution
        R = ot.Normal(4.0, 1.0)
        R.setDescription("R")
        S = ot.Normal(2.0, 1.0)
        S.setDescription("S")
        g = ot.SymbolicFunction(["R", "S"], ["R - S"])
        # Event
        inputvector = ot.ComposedDistribution([R, S])
        inputRV = ot.RandomVector(inputvector)
        outputRV = ot.CompositeRandomVector(g, inputRV)
        eventF = ot.Event(outputRV, ot.GreaterOrEqual(), 0)
        #
        # Bounds
        alphaMin = 0.01
        alphaMax = 1 - alphaMin
        lowerBound = ot.Point(
            [R.computeQuantile(alphaMin)[0], S.computeQuantile(alphaMin)[0]]
        )
        upperBound = ot.Point(
            [R.computeQuantile(alphaMax)[0], S.computeQuantile(alphaMax)[0]]
        )
        bounds = ot.Interval(lowerBound, upperBound)
        #
        drawEvent = otbenchmark.DrawEvent(eventF)
        graph = drawEvent.fillEvent(bounds)
        otv.View(graph)


if __name__ == "__main__":
    unittest.main()
