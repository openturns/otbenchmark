# -*- coding: utf-8 -*-
"""
Created on Mon May  4 13:14:27 2020

@author: Jebroun

Class to define the ReliabilityProblem63 benchmark problem.
"""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
import openturns as ot


class ReliabilityProblem63(ReliabilityBenchmarkProblem):
    def __init__(self, threshold=0.0, mu=0, sigma=1):
        """
        Creates a reliability problem RP63.

        The event is {g(X) < threshold} where

        X = (x1, x2, ...., x100)

        g(X) = 0.1 * (x2^2 + x3^2 + .... + x99^2 + x100^2) - x1 - 4.5

        We have xi ~ Normal(0, 1) for i in {1, 2, ...,100}

        Parameters
        ----------
        threshold : float
            The threshold.
        mu : float
            The mean of the Xi Normal distribution for i in {1, 2, ..., 100}.
        sigma : float
            The standard deviation of the Xi Normal distribution
            for i in {1, 2, ..., 100}.
        """

        formula = (
            " 0.1 *(x2^2 + x3^2 + x4^2 + x5^2 + x6^2 + x7^2 + x8^2 + x9^2 + x10^2 +"
        )
        formula += (
            "x11^2+ x12^2+ x13^2+ x14^2+ x15^2+ x16^2+ x17^2+ x18^2+ x19^2+x20^2+"
        )
        formula += (
            "x21^2+ x22^2+ x23^2+ x24^2+ x25^2+ x26^2+ x27^2+ x28^2+ x29^2+x30^2+"
        )
        formula += (
            "x31^2+ x32^2+ x33^2+ x34^2+ x35^2+ x36^2+ x37^2+ x38^2+ x39^2+x40^2+"
        )
        formula += (
            "x41^2+ x42^2+ x43^2+ x44^2+ x45^2+ x46^2+ x47^2+ x48^2+ x49^2+x50^2+"
        )
        formula += (
            "x51^2+ x52^2+ x53^2+ x54^2+ x55^2+ x56^2+ x57^2+ x58^2+ x59^2+x60^2+"
        )
        formula += (
            "x61^2+ x62^2+ x63^2+ x64^2+ x65^2+ x66^2+ x67^2+ x68^2+ x69^2+x70^2+"
        )
        formula += (
            "x71^2+ x72^2+ x73^2+ x74^2+ x75^2+ x76^2+ x77^2+ x78^2+ x79^2+x80^2+"
        )
        formula += (
            "x81^2+ x82^2+ x83^2+ x84^2+ x85^2+ x86^2+ x87^2+ x88^2+ x89^2+x90^2+"
        )
        formula += (
            "x91^2+ x92^2+ x93^2+ x94^2+ x95^2+ x96^2+ x97^2+ x98^2+ x99^2+x100^2)"
        )
        formula += "-4.5 - x1"

        limitStateFunction = ot.SymbolicFunction(
            [
                "x1",
                "x2",
                "x3",
                "x4",
                "x5",
                "x6",
                "x7",
                "x8",
                "x9",
                "x10",
                "x11",
                "x12",
                "x13",
                "x14",
                "x15",
                "x16",
                "x17",
                "x18",
                "x19",
                "x20",
                "x21",
                "x22",
                "x23",
                "x24",
                "x25",
                "x26",
                "x27",
                "x28",
                "x29",
                "x30",
                "x31",
                "x32",
                "x33",
                "x34",
                "x35",
                "x36",
                "x37",
                "x38",
                "x39",
                "x40",
                "x41",
                "x42",
                "x43",
                "x44",
                "x45",
                "x46",
                "x47",
                "x48",
                "x49",
                "x50",
                "x51",
                "x52",
                "x53",
                "x54",
                "x55",
                "x56",
                "x57",
                "x58",
                "x59",
                "x60",
                "x61",
                "x62",
                "x63",
                "x64",
                "x65",
                "x66",
                "x67",
                "x68",
                "x69",
                "x70",
                "x71",
                "x72",
                "x73",
                "x74",
                "x75",
                "x76",
                "x77",
                "x78",
                "x79",
                "x80",
                "x81",
                "x82",
                "x83",
                "x84",
                "x85",
                "x86",
                "x87",
                "x88",
                "x89",
                "x90",
                "x91",
                "x92",
                "x93",
                "x94",
                "x95",
                "x96",
                "x97",
                "x98",
                "x99",
                "x100",
            ],
            [formula],
        )

        X = [ot.Normal(mu, sigma) for i in range(100)]

        myDistribution = ot.ComposedDistribution(X)
        inputRandomVector = ot.RandomVector(myDistribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)

        name = "RP63"
        probability = 0.000379
        super(ReliabilityProblem63, self).__init__(name, thresholdEvent, probability)
        return None
