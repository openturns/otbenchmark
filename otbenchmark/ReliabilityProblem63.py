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
        g(X) = 0.1*(x2 + x3 + .... + x99 + x100) - x1 - 4.5.
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

        formula = " 0.1 *(x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 +"
        formula = formula + "x11+ x12+ x13+ x14+ x15+ x16+ x17+ x18+ x19+x20+"
        formula = formula + "x21+ x22+ x23+ x24+ x25+ x26+ x27+ x28+ x29+x30+"
        formula = formula + "x31+ x32+ x33+ x34+ x35+ x36+ x37+ x38+ x39+x40+"
        formula = formula + "x41+ x42+ x43+ x44+ x45+ x46+ x47+ x48+ x49+x50+"
        formula = formula + "x51+ x52+ x53+ x54+ x55+ x56+ x57+ x58+ x59+x60+"
        formula = formula + "x61+ x62+ x63+ x64+ x65+ x66+ x67+ x68+ x69+x70+"
        formula = formula + "x71+ x72+ x73+ x74+ x75+ x76+ x77+ x78+ x79+x80+"
        formula = formula + "x81+ x82+ x83+ x84+ x85+ x86+ x87+ x88+ x89+x90+"
        formula = formula + "x91+ x92+ x93+ x94+ x95+ x96+ x97+ x98+ x99+x100)"
        formula = formula + "-4.5 - x1"

        print(formula)
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
