"""
Manage reliability problems.
"""
import otbenchmark as otb
import numpy as np
import sys


def ComputeLogRelativeError(exact, computed, basis=10.0):
    r"""
    Compute the log-relative error between exact and computed.

    The log-relative error (LRE) is defined by:

    .. math::

        LRE = -logB(relativeError)

    where relativeError is the relative error:

    .. math::

        relativeError = \frac{|exact - computed|}{|exact|}

    and logB is the base-b logarithm:

    .. math::

        logB(x) = \frac{log(x)}{log(basis)}

    where log is the natural logarithm.
    This assumes that exact is different from zero.

    The LRE is the number of base-B common digits in exact and computed,
    if the exponents are the same.
    Otherwise, the LRE can be large (i.e. the number of "common digits" can
    be large), even if the digits are very
    different.
    For example, if exact = 1.00000000000 and computed = 0.99999999999,
    then LRE = 11 even if there is no common digits in the two real
    numbers.

    Parameters
    ----------
    exact: float
        The exact value.
    computed: float
        The computed value.

    Returns
    -------
    logRelativeError: float
        The LRE.
        The maximum possible LRE is 15.65.
        The minimum possible LRE is 0.

    Examples
    --------
    >>> import otbenchmark as otb
    >>> benchmarkProblemList = otb.ReliabilityBenchmarkProblemList()
    >>> numberOfProblems = len(benchmarkProblemList)
    >>> for i in range(numberOfProblems):
    ...     problem = benchmarkProblemList[i]
    ...     name = problem.getName()
    ...     pf = problem.getProbability()
    ...     print("#", i, " : ", name, ", exact PF : ", pf)
    """
    if abs(exact) == 0.0:
        # Avoid division by zero
        logRelativeError = 0.0
    elif abs(exact) > sys.float_info.max:
        # Avoid generating NANs
        logRelativeError = 0.0
    else:
        relativeError = abs(exact - computed) / abs(exact)
        relativeError = max(relativeError, sys.float_info.epsilon)
        logRelativeError = -np.log(relativeError) / np.log(basis)
        # https://github.com/mbaudin47/otbenchmark/issues/86
        logRelativeError = abs(max(logRelativeError, 0.0))
    return logRelativeError


def ComputeAbsoluteError(exact, computed):
    """
    Compute absolute error between exact and computed.

    The absolute error is defined by:

    absoluteError = abs(exact - computed).

    Parameters
    ----------
    exact : float
        The exact value.
    computed : float
        The computed value.

    Returns
    -------
    absoluteError : float
        The absolute error.
    """
    absoluteError = abs(exact - computed)
    return absoluteError


def ComputeRelativeError(exact, computed):
    """
    Compute relative error between exact and computed.

    The relative error is defined by:

        relativeError = abs(exact - computed) / abs(exact)

    if exact is different from zero.

    Parameters
    ----------
    exact: float
        The exact value.
    computed: float
        The computed value.

    Returns
    -------
    relativeError: float
        The relative error.
    """
    relativeError = abs(exact - computed) / abs(exact)
    return relativeError


def ReliabilityBenchmarkProblemList():
    """
    Returns the list of reliability benchmark problems.

    Returns
    -------
    problems : list
        A list of ReliabilityProblem.
    """
    p8 = otb.ReliabilityProblem8()
    p14 = otb.ReliabilityProblem14()
    p22 = otb.ReliabilityProblem22()
    p24 = otb.ReliabilityProblem24()
    p25 = otb.ReliabilityProblem25()
    p28 = otb.ReliabilityProblem28()
    p31 = otb.ReliabilityProblem31()
    p33 = otb.ReliabilityProblem33()
    p35 = otb.ReliabilityProblem35()
    p38 = otb.ReliabilityProblem38()
    p53 = otb.ReliabilityProblem53()
    p55 = otb.ReliabilityProblem55()
    p54 = otb.ReliabilityProblem54()
    p57 = otb.ReliabilityProblem57()
    p75 = otb.ReliabilityProblem75()
    p89 = otb.ReliabilityProblem89()
    p107 = otb.ReliabilityProblem107()
    p110 = otb.ReliabilityProblem110()
    p111 = otb.ReliabilityProblem111()
    p63 = otb.ReliabilityProblem63()
    p91 = otb.ReliabilityProblem91()
    p60 = otb.ReliabilityProblem60()
    p77 = otb.ReliabilityProblem77()
    pFBS = otb.FourBranchSerialSystemReliability()
    pRS = otb.RminusSReliability()
    pBeam = otb.AxialStressedBeamReliability()
    problemslist = [
        p8,
        p14,
        p22,
        p24,
        p25,
        p28,
        p31,
        p33,
        p35,
        p38,
        p53,
        p55,
        p54,
        p57,
        p75,
        p89,
        p107,
        p110,
        p111,
        p63,
        p91,
        p60,
        p77,
        pFBS,
        pRS,
        pBeam,
    ]
    return problemslist
