#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define a benchmark problem using http requests from the BBRC 2019 server."""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
from otbenchmark.BBRCDistribution import BBRCDistribution
from otbenchmark import evaluate
import openturns as ot
import numpy as np


class RequestedBBRCProblem(ReliabilityBenchmarkProblem):
    def __init__(self, username, password, set_id, problem_id):
        """
        Creates a ot.PythonFunction requesting a BBRC 2019 function using http requests.
        References
        ----------
        https://rprepo.readthedocs.io/en/latest/
        Parameters
        ----------
        username: str
            Username required to login the BBRC challenge.
        password: str
            Password required to login the BBRC challenge.
        set_id: int
            First item defining the reliability problem selected.
        problem_id: int
            Second item defining the reliability problem selected.
        """
        self.username = username
        self.password = password
        self.set_id = set_id
        self.problem_id = problem_id

        def g_fun(x):
            x = np.array(x)
            g_val_sys, g_val_comp, msg = evaluate.evaluate(
                self.username, self.password, self.set_id, self.problem_id, x
            )
            return g_val_comp

        # BBRCDistribution
        my_dist = BBRCDistribution(self.set_id, self.problem_id)
        inputDistribution = my_dist.build_composed_dist()
        inputRandomVector = ot.RandomVector(inputDistribution)
        input_dim = inputDistribution.getDimension()
        # BBRCResults
        types = ["i4", "i4", "i4", "f8"]
        bbrc_result_table = np.genfromtxt(
            "./distributions/beta_results.csv", dtype=types, delimiter=",", names=True
        )
        my_result = bbrc_result_table[
            (bbrc_result_table["problem_id"] == self.problem_id)
            & (bbrc_result_table["set_id"] == self.set_id)
        ]
        name = "RP" + str(my_result["reliability_problem_id"][0])
        beta = my_result["beta"][0]
        limitStateFunction = ot.PythonFunction(input_dim, 1, g_fun)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), 0.0)

        probability = ot.Normal().computeComplementaryCDF(beta)
        super(RequestedBBRCProblem, self).__init__(name, thresholdEvent, probability)

        return None
