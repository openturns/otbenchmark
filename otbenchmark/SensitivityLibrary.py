#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manage sensitivity problems.
"""
import otbenchmark as otb


def SensitivityBenchmarkProblemList():
    """
    Returns the list of sensitivity analysis benchmark problems.

    Returns
    -------
    problems : list
        A list of SensitivityProblem.

    Examples
    --------
    >>> import otbenchmark as otb
    >>> benchmarkProblemList = otb.SensitivityBenchmarkProblemList()
    >>> numberOfProblems = len(benchmarkProblemList)
    >>> for i in range(numberOfProblems):
    ...     problem = benchmarkProblemList[i]
    ...     name = problem.getName()
    ...     first_order_indices = problem.getFirstOrderIndices()
    ...     total_order_indices = problem.getTotalOrderIndices()
    ...     dimension = problem.getInputDistribution().getDimension()
    ...     print("#", i, ":", name, " : S = ", first_order_indices,
    ...           "T=", total_order_indices, ", dimension=", dimension)
    """
    problemslist = [
        otb.GaussianSumSensitivity(),
        otb.GaussianProductSensitivity(),
        otb.GSobolSensitivity(),
        otb.IshigamiSensitivity(),
        otb.BoreholeSensitivity(),
        otb.DirichletSensitivity(),
        otb.FloodingSensitivity(),
        otb.MorrisSensitivity(),
        otb.NLOscillatorSensitivity(),
        otb.BorgonovoSensitivity(),
        otb.OakleyOHaganSensitivity(),
    ]
    return problemslist
