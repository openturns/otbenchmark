#!/usr/bin/env python
# -*- coding: utf-8 -*-


import openturns as ot
import numpy as np
import pandas as pd


def run_FORM_simple(
    event,
    inputDistribution,
    nearestPointAlgo="AbdoRackwitz",
    NmaxIteration=100,
    eps=[1e-5] * 4,
    physicalStartingPoint=None,
    seed=1234,
    verbose=False,
):

    """
    Run a FORM approximation.

    Parameters
    ----------
    event : openturns.Event
        The failure event.
    inputDistribution : openturns.distribution
        The distribution of the event.
    nearestPointAlgo : str
        Type of the optimization algorithm. It must be 'AbdoRackwitz', 'SQP' or
        'Cobyla'.
    NmaxIteration : int
        The maximum number of iterations.
    eps = sequence of float
        The stopping criterion value of the optimization algorithm. Order is
        absolute error, relative error, residual error, constraint error.
    physicalStartingPoint : sequence of float
        The starting point of the algorithm. Default is the median values.
    seed : int
        Seed for the openturns random generator.
    logfile : bool
        Enable or not to write the log in FORM.log file.
    verbose : bool
        Enable or not the display of the result.
    activeCache : bool
        Enable or not the cache mechanism of the NumericalMathFunction.
    activeHistory : bool
        Enable or not the history mechanism of the NumericalMathFunction.
    """

    # Initialize the random generator
    ot.RandomGenerator.SetSeed(seed)

    # Defintion of the nearest point algorithm
    if nearestPointAlgo == "AbdoRackwitz":
        solver = ot.AbdoRackwitz()
        # spec = algo.getSpecificParameters()
        # spec.setTau(0.5)
        # algo.setSpecificParameters(spec)
    elif nearestPointAlgo == "Cobyla":
        solver = ot.Cobyla()
    elif nearestPointAlgo == "SQP":
        solver = ot.SQP()
    else:
        raise NameError(
            "Nearest point algorithm name must be \
                            'AbdoRackwitz', 'Cobyla' or 'SQP'."
        )

    eps = np.array(eps)
    solver.setMaximumAbsoluteError(eps[0])
    solver.setMaximumRelativeError(eps[1])
    solver.setMaximumResidualError(eps[2])
    solver.setMaximumConstraintError(eps[3])
    solver.setMaximumIterationNumber(NmaxIteration)

    # Set the physical starting point of the Nearest point
    # algorithm to the mediane value
    if physicalStartingPoint is None:
        physicalStartingPoint = inputDistribution.getMean()

    # Run FORM method
    approximation = ot.FORM(solver, event, physicalStartingPoint)
    approximation.run()
    result = approximation.getResult()
    optimResult = result.getOptimizationResult()
    iter_number = optimResult.getIterationNumber()

    dfResult = pd.DataFrame()
    dfResult = dfResult.append(
        pd.DataFrame([result.getEventProbability()], index=["Probability of failure"])
    )
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getGeneralisedReliabilityIndex()],
            index=["Generalised reliability index"],
        )
    )
    dfResult = dfResult.append(
        pd.DataFrame([iter_number], index=["Number of iterations"])
    )
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getStandardSpaceDesignPoint()],
            index=["Standard space design point"],
        )
    )
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getPhysicalSpaceDesignPoint()],
            index=["Physical space design point"],
        )
    )

    dfResult = dfResult.reset_index()
    dfResult.columns = ["", "Results - FORM (" + nearestPointAlgo + ")"]
    pd.options.display.float_format = "{:,.2E}".format
    if verbose:
        print(dfResult, "\n")

    return approximation


class FORMsystem:
    """
    This class aims at computing the probability of failure of a structure with
    several most probable failure points.

    Parameters:
    -----------
    FORMruns : list of openturns.FORM object
        The list of the FORM objects which have been run.
    failure_domain : string
        Type of failure domain form : either 'union' or 'intersection'.
    """

    def __init__(self, FORMruns, failure_domain="union"):

        self._nFORM = len(FORMruns)
        self._FORMresult = [FORMruns[i].getResult() for i in range(self._nFORM)]
        self._beta = None
        self._ustar = None
        self._alpha = None
        self._rho = None
        self._failure_domain = failure_domain

    def _getBeta(self):
        self._beta = [
            self._FORMresult[i].getGeneralisedReliabilityIndex()
            for i in range(self._nFORM)
        ]
        return self._beta

    def getStandardSpaceDesignPoint(self):
        self._ustar = [
            self._FORMresult[i].getStandardSpaceDesignPoint()
            for i in range(self._nFORM)
        ]
        return self._ustar

    def getPhysicalSpaceDesignPoint(self):
        self._ustar = [
            self._FORMresult[i].getPhysicalSpaceDesignPoint()
            for i in range(self._nFORM)
        ]
        return self._ustar

    def getAlpha(self):

        if self._beta is None:
            self._getBeta()

        if self._ustar is None:
            self.getStandardSpaceDesignPoint()

        self._alpha = [
            self._ustar[i] / (-self._beta[i]) for i in range(len(self._ustar))
        ]
        return self._alpha

    def _getRho(self):

        if self._alpha is None:
            self.getAlpha()

        dim = len(self._alpha)
        self._rho = ot.CorrelationMatrix(dim)

        for i in range(dim):
            for j in range(dim):
                if i < j:
                    self._rho[i, j] = np.dot(self._alpha[i], self._alpha[j])

        return self._rho

    def getEventProbability(self):
        """
        Accessor the event probability

        Returns
        -------
        pf : float
            The FORM system probability.
        """

        if self._rho is None:
            self._getRho()

        dim = len(self._alpha)
        multiNor = ot.Normal([0] * dim, [1] * dim, self._rho)

        if self._failure_domain == "union":
            pf = 1 - multiNor.computeCDF(self._beta)
        elif self._failure_domain == "intersection":
            pf = multiNor.computeCDF(-np.array(self._beta))

        return pf

    def getHasoferReliabilityIndex(self):
        """
        Accessor to the equivalent reliability index

        Returns
        -------
        beta : float
            The reliability index.
        """
        return ot.DistFunc.qNormal(1.0 - self.getEventProbability())


def run_FORM(event, distribution, failure_domain=None, **kwargs):
    """
    Run a FORM approximation system or not.

    Parameters
    ----------
    event : openturns.Event or a list of openturns.Event
        The failure event or the list of event defining the limit state.
    inputDistribution : openturns.distribution
        The distribution of the event.
    nearestPointAlgo : str
        Type of the optimization algorithm. It must be 'AbdoRackwitz', 'SQP' or
        'Cobyla'.
    NmaxIteration : int
        The maximum number of iterations.
    eps = sequence of float
        The stopping criterion value of the optimization algorithm. Order is
        absolute error, relative error, residual error, constraint error.
    physicalStartingPoint : sequence of float
        The starting point of the algorithm. Default is the median values.
    seed : int
        Seed for the openturns random generator.
    logfile : bool
        Enable or not to write the log in FORM.log file.
    verbose : bool
        Enable or not the display of the result.
    activeCache : bool
        Enable or not the cache mechanism of the NumericalMathFunction.
    activeHistory : bool
        Enable or not the history mechanism of the NumericalMathFunction.
    failure_domain : string
        Type of failure domain form : either 'union' or 'intersection'.
    """

    if type(event) is list:
        FORMruns = []
        for event_solo in event:
            FORMruns.append(run_FORM_simple(event_solo, distribution, **kwargs))

        return FORMsystem(FORMruns, failure_domain)
    else:
        return run_FORM_simple(event, distribution, **kwargs).getResult()
