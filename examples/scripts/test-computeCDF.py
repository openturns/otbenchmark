#!/usr/bin/env python3
"""
This script shows how to use the computeCDF method in order
to compute exact probabilities using Distribution arithmetic.
"""

# Creates a reliability problem RP8.
import otbenchmark as otb
import numpy as np


def ComputeReferenceProbability(problem, verbose=False):
    """
    Compute the probability of a reliability problem using computeCDF().

    Parameters
    ----------
    problem : ot.ReliabilityProblem
        The problem.
    verbose : bool, optional
        If True, print messages. The default is False.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    pf : float
        The probability of failure.

    """
    event = problem.getEvent()
    antecedent = event.getAntecedent()
    distribution = antecedent.getDistribution()
    # Check copula
    copula = distribution.getCopula()
    if not copula.hasIndependentCopula():
        raise Exception("Copula is not independent.")
    # Set marginal distribution X0, X1, etc... up to Xd
    description = distribution.getDescription()
    dimension = distribution.getDimension()
    for i in range(dimension):
        marginal = distribution.getMarginal(i)
        marginal_statement = "%s = marginal" % (description[i])
        if verbose and i < 5:
            print("marginal = ", marginal)
            print(marginal_statement)
        exec(marginal_statement)
    # Prepare constants and functions
    PI_ = np.pi
    _ = PI_  # To fool flake8

    def SQRT(x):
        return np.sqrt(x)

    def MIN(x, y):
        return min(x, y)

    def ABS(x):
        return abs(x)

    # Get the formula
    function = event.getFunction()
    function_repr = str(function)
    start = function_repr.find(">")
    formula = function_repr[start + 2 : -1]
    formula = formula.upper()
    formula_Y = "Y = " + formula
    # Replace ExprTk "^" with Python-style "**"
    formula_Y = formula_Y.replace("^", "**")
    if verbose:
        print(formula_Y)
    exec(formula_Y)
    # Compute pdf
    threshold = event.getThreshold()
    _ = threshold  # To fool flake8
    pf = eval("Y.computeCDF(threshold)")
    return pf


# Fails on RP14
# https://github.com/openturns/openturns/issues/1720
# problem = otb.ReliabilityProblem14()
# pf_formula = ComputeReferenceProbability(problem, verbose=True)

verbose = False
benchmarkProblemList = otb.ReliabilityBenchmarkProblemList()
numberOfProblems = len(benchmarkProblemList)

for i in range(numberOfProblems):
    problem = benchmarkProblemList[i]
    name = problem.getName()
    if name == "RP14":
        continue
    if name == "RP38":
        continue
    pf_reference = problem.getProbability()
    print(i, ":", name, "...")
    try:
        pf_formula = ComputeReferenceProbability(problem, verbose=verbose)
        lre = otb.ComputeLogRelativeError(pf_formula, pf_reference)
        print(
            "#",
            i,
            ":",
            name,
            ", Pf_ref =",
            pf_reference,
            ", Pf - Formula=",
            pf_formula,
            ", lre =",
            lre,
        )
    except Exception as inst:
        print("#", i, ":", name)
        print("    Fails")
        print("    ", inst)
