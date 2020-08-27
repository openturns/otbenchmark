#!/usr/bin/env python
# -*- coding: utf-8 -*-


import openturns as ot
import numpy as np
import pandas as pd


def run_MonteCarlo(
    event,
    coefVar=0.1,
    outerSampling=10000,
    blockSize=10,
    seed=1234,
    verbose=False,
    failure_domain=None,
):

    """
    Run a Monte Carlo simulation.

    Parameters
    ----------
    event : openturns.Event
        The failure event or a list of failure event.
    coefVar : float
         The target coefficient of variation.
    outerSampling : int
        The maximum number of outer iterations.
        Nb of iterations = outerSampling x blockSize.
    blockSize : int
        The number of samples send to evaluate simultaneously.
    seed : int
        Seed for the openturns random generator.
    logfile : bool
        Enable or not to write the log in MonteCarlo.log file.
    verbose : bool
        Enable or not the display of the result.
    activeCache : bool
        Enable or not the cache mechanism of the NumericalMathFunction.
    activeHistory : bool
        Enable or not the history mechanism of the NumericalMathFunction.
    failure_domain : string
        Type of failure domain form : either 'union' or 'intersection'. Only
        needed if the event is a list.
    """

    # case with the limit state defined as an intersection or a
    # union of the event
    if type(event) is list:
        n_event = len(event)
        antecedent = event[0].getAntecedent()

        if failure_domain == "union":

            def function_union(X):
                sample = ot.NumericalSample(X.getSize(), n_event)
                for i in range(n_event):
                    sample[:, i] = event[i].getFunction()(X)

                sample = np.array(sample)
                for i in range(n_event):
                    if (
                        event[i].getOperator().getImplementation().getClassName()
                        == "Less"
                        or event[i].getOperator().getImplementation().getClassName()
                        == "LessOrEqual"
                    ):
                        sample[:, i] = sample[:, i] < event[i].getThreshold()
                    if (
                        event[i].getOperator().getImplementation().getClassName()
                        == "Greater"
                        or event[i].getOperator().getImplementation().getClassName()
                        == "GreaterOrEqual"
                    ):
                        sample[:, i] = sample[:, i] >= event[i].getThreshold()
                return np.atleast_2d(sample.sum(axis=1)).T

            model = ot.PythonFunction(
                event[0].getFunction().getInputDimension(),
                event[0].getFunction().getOutputDimension(),
                func_sample=function_union,
            )
            output = ot.RandomVector(model, antecedent)
            event = ot.Event(output, ot.Greater(), 0.0)

        elif failure_domain == "intersection":

            def function_intersection(X):
                sample = ot.NumericalSample(X.getSize(), n_event)
                for i in range(n_event):
                    sample[:, i] = event[i].getFunction()(X)

                sample = np.array(sample)
                for i in range(n_event):
                    if (
                        event[i].getOperator().getImplementation().getClassName()
                        == "Less"
                        or event[i].getOperator().getImplementation().getClassName()
                        == "LessOrEqual"
                    ):
                        sample[:, i] = sample[:, i] < event[i].getThreshold()
                    if (
                        event[i].getOperator().getImplementation().getClassName()
                        == "Greater"
                        or event[i].getOperator().getImplementation().getClassName()
                        == "GreaterOrEqual"
                    ):
                        sample[:, i] = sample[:, i] >= event[i].getThreshold()
                return np.atleast_2d(sample.prod(axis=1)).T

            model = ot.PythonFunction(
                event[0].getFunction().getInputDimension(),
                event[0].getFunction().getOutputDimension(),
                func_sample=function_intersection,
            )
            output = ot.RandomVector(model, antecedent)
            new_event = ot.Event(output, ot.Greater(), 0.0)
    else:
        model = event.getFunction()
        new_event = event

    # Initialize the random generator
    ot.RandomGenerator.SetSeed(seed)

    # Run Monte Carlo simulation
    experiment = ot.MonteCarloExperiment()
    simulation = ot.ProbabilitySimulationAlgorithm(new_event, experiment)
    simulation.setMaximumCoefficientOfVariation(coefVar)
    simulation.setMaximumOuterSampling(outerSampling)
    simulation.setBlockSize(blockSize)

    # try:
    simulation.run()
    # except Exception as e:
    #     dump_cache(model, 'Cache/physicalModelMathFunction')
    #     raise e

    result = simulation.getResult()

    dfResult = pd.DataFrame()
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getProbabilityEstimate()], index=["Probability of failure"]
        )
    )
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getCoefficientOfVariation()], index=["Coefficient of varation"],
        )
    )
    dfResult = dfResult.append(
        pd.DataFrame([result.getConfidenceLength()], index=["95 % Confidence length"])
    )
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getOuterSampling() * result.getBlockSize()],
            index=["Number of calls"],
        )
    )
    dfResult = dfResult.reset_index()
    dfResult.columns = ["", "Results - Monte Carlo"]

    if verbose:
        print(dfResult, "\n")

    return simulation


def run_ImportanceSampling(
    event,
    pstar,
    sd=1.0,
    coefVar=0.05,
    outerSampling=1000,
    blockSize=10,
    seed=1234,
    verbose=False,
    failure_domain=None,
):
    """
    Run an importance sampling simulation.

    Parameters
    ----------
    event : openturns.Event
        The failure event.
    pstar : list of points
        Design points in the standard space where to centered the instrumental
        distribution.
    sd : positive float
        The standard deviation of the instrumental distribution.
    coefVar : float
         The target coefficient of variation.
    outerSampling : int
        The maximum number of outer iterations.
        Nb of iterations = outerSampling x blockSize.
    blockSize : int
        The number of samples send to evaluate simultaneously.
    seed : int
        Seed for the openturns random generator.
    logfile : bool
        Enable or not to write the log in ImportanceSampling.log file.
    verbose : bool
        Enable or not the display of the result.
    activeCache : bool
        Enable or not the cache mechanism of the NumericalMathFunction.
    activeHistory : bool
        Enable or not the history mechanism of the NumericalMathFunction.
    failure_domain : string
        Type of failure domain form : either 'union' or 'intersection'. Only
        needed if the event is a list.
    """

    # case with the limit state defined as an intersection
    # or a union of the event
    if type(event) is list:
        n_event = len(event)
        antecedent = event[0].getAntecedent()

        if failure_domain == "union":

            def function_union(X):
                sample = ot.NumericalSample(X.getSize(), n_event)
                for i in range(n_event):
                    sample[:, i] = event[i].getFunction()(X)

                sample = np.array(sample)
                for i in range(n_event):
                    if (
                        event[i].getOperator().getImplementation().getClassName()
                        == "Less"
                        or event[i].getOperator().getImplementation().getClassName()
                        == "LessOrEqual"
                    ):
                        sample[:, i] = sample[:, i] < event[i].getThreshold()
                    if (
                        event[i].getOperator().getImplementation().getClassName()
                        == "Greater"
                        or event[i].getOperator().getImplementation().getClassName()
                        == "GreaterOrEqual"
                    ):
                        sample[:, i] = sample[:, i] >= event[i].getThreshold()
                return np.atleast_2d(sample.sum(axis=1)).T

            model = ot.PythonFunction(
                event[0].getFunction().getInputDimension(),
                event[0].getFunction().getOutputDimension(),
                func_sample=function_union,
            )
            output = ot.RandomVector(model, antecedent)
            event = ot.Event(output, ot.Greater(), 0.0)

        elif failure_domain == "intersection":

            def function_intersection(X):
                sample = ot.NumericalSample(X.getSize(), n_event)
                for i in range(n_event):
                    sample[:, i] = event[i].getFunction()(X)

                sample = np.array(sample)
                for i in range(n_event):
                    if (
                        event[i].getOperator().getImplementation().getClassName()
                        == "Less"
                        or event[i].getOperator().getImplementation().getClassName()
                        == "LessOrEqual"
                    ):
                        sample[:, i] = sample[:, i] < event[i].getThreshold()
                    if (
                        event[i].getOperator().getImplementation().getClassName()
                        == "Greater"
                        or event[i].getOperator().getImplementation().getClassName()
                        == "GreaterOrEqual"
                    ):
                        sample[:, i] = sample[:, i] >= event[i].getThreshold()
                return np.atleast_2d(sample.prod(axis=1)).T

            model = ot.PythonFunction(
                event[0].getFunction().getInputDimension(),
                event[0].getFunction().getOutputDimension(),
                func_sample=function_intersection,
            )
            output = ot.RandomVector(model, antecedent)
            new_event = ot.Event(output, ot.Greater(), 0.0)
    else:
        model = event.getFunction()
        new_event = event

    # Initialize the random generator
    ot.RandomGenerator.SetSeed(seed)

    dim = model.getInputDimension()
    pstar = np.atleast_2d(pstar)
    nPoint = pstar.shape[0]

    stdev = [sd] * dim
    corr = ot.IdentityMatrix(dim)
    if nPoint > 1:
        distribution_list = list()
        for point in pstar:
            distribution_list.append(ot.Normal(point, stdev, corr))
        instrumental_distribution = ot.Mixture(distribution_list)
    elif nPoint == 1:
        instrumental_distribution = ot.Normal(pstar[0], stdev, corr)

    # Run importance sampling simulation
    experiment = ot.ImportanceSamplingExperiment(instrumental_distribution)
    simulation = ot.ProbabilitySimulationAlgorithm(
        ot.StandardEvent(new_event), experiment
    )
    simulation.setMaximumOuterSampling(outerSampling)
    simulation.setBlockSize(blockSize)
    simulation.setMaximumCoefficientOfVariation(coefVar)

    # try:
    simulation.run()
    # except Exception as e:
    #     dump_cache(model, 'Cache/physicalModelMathFunction')
    #     raise e

    result = simulation.getResult()

    dfResult = pd.DataFrame()
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getProbabilityEstimate()], index=["Probability of failure"]
        )
    )
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getCoefficientOfVariation()], index=["Coefficient of varation"],
        )
    )
    dfResult = dfResult.append(
        pd.DataFrame([result.getConfidenceLength()], index=["95 % Confidence length"])
    )
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getOuterSampling() * result.getBlockSize()],
            index=["Number of calls"],
        )
    )
    dfResult = dfResult.reset_index()
    dfResult.columns = ["", "Results - Importance Sampling"]

    if verbose:
        print(dfResult, "\n")

    return simulation


def run_LHS(
    event,
    coefVar=0.01,
    outerSampling=1000,
    seed=1234,
    verbose=False,
    failure_domain=None,
):

    """
    Run a LHS simulation
    """

    # Initialize the random generator
    ot.RandomGenerator.SetSeed(seed)

    # Run LHS simulation

    # ~ LHS = ot.LHSExperiment()
    # ~ LHS.setAlwaysShuffle(True)
    # ~ SA_profile = ot.GeometricProfile(10., 0.95, 20000)
    # ~ LHS_opt = ot.SimulatedAnnealingLHS(LHS, SA_profile,
    #                                      ot.SpaceFillingC2())
    # ~ LHS_opt.generate()
    # ~ LHS_design = LHS_opt.getResult()
    # ~ LHS_design = LHS_design.getOptimalDesign()
    # ~ simulation = ot.ProbabilitySimulationAlgorithm(new_event, LHS_design)

    simulation = ot.LHS(event)
    simulation.setMaximumCoefficientOfVariation(coefVar)
    simulation.setMaximumOuterSampling(outerSampling)
    # simulation.setBlockSize(blockSize)

    # try:
    simulation.run()
    # except Exception as e:
    #     dump_cache(model, 'Cache/physicalModelMathFunction')
    #     raise e

    result = simulation.getResult()

    dfResult = pd.DataFrame()
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getProbabilityEstimate()], index=["Probability of failure"]
        )
    )
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getCoefficientOfVariation()], index=["Coefficient of varation"],
        )
    )
    dfResult = dfResult.append(
        pd.DataFrame([result.getConfidenceLength()], index=["95 % Confidence length"])
    )
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getOuterSampling() * result.getBlockSize()],
            index=["Number of calls"],
        )
    )
    dfResult = dfResult.reset_index()
    dfResult.columns = ["", "Results - LHS"]

    if verbose:
        print(dfResult, "\n")
    return simulation


def run_SubSet(
    event,
    coefVar=0.05,
    outerSampling=1000,
    seed=1234,
    verbose=False,
    failure_domain=None,
):

    """
    Run a Subset simulation
    """
    # Initialize the random generator
    ot.RandomGenerator.SetSeed(seed)

    # Run LHS simulation
    simulation = ot.SubsetSampling(event, 2.0, 0.05)
    simulation.setMaximumCoefficientOfVariation(coefVar)
    simulation.setMaximumOuterSampling(outerSampling)
    # simulation.setBlockSize(blockSize)

    # try:
    simulation.run()
    # except Exception as e:
    #     dump_cache(model, 'Cache/physicalModelMathFunction')
    #     raise e

    result = simulation.getResult()

    dfResult = pd.DataFrame()
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getProbabilityEstimate()], index=["Probability of failure"]
        )
    )
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getCoefficientOfVariation()], index=["Coefficient of varation"],
        )
    )
    dfResult = dfResult.append(
        pd.DataFrame([result.getConfidenceLength()], index=["95 % Confidence length"])
    )
    dfResult = dfResult.append(
        pd.DataFrame(
            [result.getOuterSampling() * result.getBlockSize()],
            index=["Number of calls"],
        )
    )
    dfResult = dfResult.reset_index()
    dfResult.columns = ["", "Results - Subset"]

    if verbose:
        print(dfResult, "\n")
    return simulation
