# -*- coding: utf-8 -*-
# Copyright 2020 EDF
"""
Test for ReliabilityBenchmarkProblem class.
"""
import otbenchmark as otb
import unittest
import openturns as ot


class CheckReliabilityBenchmarkProblem(unittest.TestCase):
    def test_ReliabilityBenchmarkProblem(self):
        limitStateFunction = ot.SymbolicFunction(["R", "S"], ["R - S"])

        muR = 4.0
        sigmaR = 1.0
        muS = 2.0
        sigmaS = 1.0
        threshold = 0.0
        R = ot.Normal(muR, sigmaR)
        S = ot.Normal(muS, sigmaS)
        myDistribution = ot.ComposedDistribution([R, S])
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "R-S"
        probability = 0.123456789
        problem = otb.ReliabilityBenchmarkProblem(name, thresholdEvent, probability)
        #
        print(problem)
        print(problem.toFullString())
        p = problem.getProbability()
        assert p == probability
        s = problem.getName()
        assert s == name


if __name__ == "__main__":
    unittest.main()
