#!/usr/bin/python
# coding:utf-8
# Copyright 2020 EDF
"""Class to define a benchmark problem using http requests from the BBRC 2019 server."""

from otbenchmark.ReliabilityBenchmarkProblem import ReliabilityBenchmarkProblem
from otbenchmark import evaluate
import openturns as ot
import pandas as pd
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
        self.problem_id  = problem_id

        def g_fun(x):
            x = np.array(x)
            g_val_sys, g_val_comp, msg = evaluate.evaluate(self.username, \
                                self.password, self.set_id, self.problem_id, x)
            print(g_val_comp)
            return g_val_comp

        bbrc_problem_table = pd.DataFrame([], columns=["name", "set_id", "problem_id", \
                "input_dim", "output_dim", "beta", "input_composed_distribution"])
        bbrc_problem_table = bbrc_problem_table.astype("object")
        #import a csv with all the corresponding elements. Next line is for the example corresponding to the RP8
        bbrc_problem_table.loc[0] = ["RP 8", -1, 1, 6, 1, 3.16, \
                ot.ComposedDistribution((ot.ParametrizedDistribution(ot.LogNormalMuSigma(120, 12)), \
                                        ot.ParametrizedDistribution(ot.LogNormalMuSigma(120, 12)), \
                                        ot.ParametrizedDistribution(ot.LogNormalMuSigma(120, 12)), \
                                        ot.ParametrizedDistribution(ot.LogNormalMuSigma(120, 12)), \
                                        ot.ParametrizedDistribution(ot.LogNormalMuSigma(50, 10)), \
                                        ot.ParametrizedDistribution(ot.LogNormalMuSigma(40, 8))\
                                        ))
                                    ]
        bbrc_problem_raw = bbrc_problem_table[(bbrc_problem_table["problem_id"]==self.problem_id)\
                                         & (bbrc_problem_table["set_id"]==self.set_id)]
        input_dim = int(bbrc_problem_raw["input_dim"])
        output_dim = int(bbrc_problem_raw["output_dim"])
        inputDistribution = bbrc_problem_raw["input_composed_distribution"][0]
        inputRandomVector = ot.RandomVector(inputDistribution)

        limitStateFunction = ot.PythonFunction(input_dim, output_dim, g_fun)
        outputRandomVector = ot.CompositeRandomVector(limitStateFunction, inputRandomVector)
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), 0.0)

        name = bbrc_problem_raw["name"]
        beta = bbrc_problem_raw["beta"]
        probability = ot.Normal().computeComplementaryCDF(beta)        
        super(RequestedBBRCProblem, self).__init__(name, thresholdEvent, probability)
        
        return None
