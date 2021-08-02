#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manage sensitivity problems.
"""
import otbenchmark as otb
import openturns as ot
import numpy as np
import time


def SensitivityBenchmarkProblemList():
    """
    Returns the list of sensitivity analysis benchmark problems.

    Returns
    -------
    problems : list
        A list of SensitivityProblem.

    Example
    -------
    import otbenchmark as otb
    benchmarkProblemList = otb.SensitivityBenchmarkProblemList()
    numberOfProblems = len(benchmarkProblemList)
    for i in range(numberOfProblems):
        problem = benchmarkProblemList[i]
        name = problem.getName()
        first_order_indices = problem.getFirstOrderIndices()
        total_order_indices = problem.getTotalOrderIndices()
        dimension = problem.getInputDistribution().getDimension()
        print("#", i, ":", name, " : S = ", first_order_indices,
              "T=", total_order_indices, ", dimension=", dimension)
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


def compute_AE_by_sampling(problem, sample_size, estimator="Saltelli"):
    """
    Compute the absolute error for the given problem with Monte-Carlo sample.

    Uses Saltelli estimator.

    For some cases, the reference Sobol' index is zero.
    This is why the relative error cannot be used as a metric.
    We compute the absolute error between the reference Sobol'
    indices and the computed Sobol' indices:

        AE(i) = abs(S_computed(i) - S_reference(i))

    for i = 1, ..., p where p is the dimension of the problem.

    Parameters
    ----------
    problem : otbenchmark.SensitivityBenchmarkProblem
        The problem to solve.
    sample_size : int
        The size of the Monte-Carlo sample.
    estimator : str
        The name of the estimator.
        Can be "Saltelli", "Martinez", "Jansen", "MauntzKucherenko".

    Returns
    -------
    first_order_AE : ot.Point(dimension)
        The AE of the first order Sobol' indices.
    total_order_AE : ot.Point(dimension)
        The AE of the total order Sobol' indices.
    """
    distribution = problem.getInputDistribution()
    model = problem.getFunction()
    # Create X/Y data
    inputDesign = ot.SobolIndicesExperiment(distribution, sample_size).generate()
    outputDesign = model(inputDesign)
    if estimator == "Saltelli":
        # Compute first order indices using the Saltelli estimator
        sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(
            inputDesign, outputDesign, sample_size
        )
    elif estimator == "Martinez":
        sensitivityAnalysis = ot.MartinezSensitivityAlgorithm(
            inputDesign, outputDesign, sample_size
        )
    elif estimator == "Jansen":
        sensitivityAnalysis = ot.JansenSensitivityAlgorithm(
            inputDesign, outputDesign, sample_size
        )
    elif estimator == "MauntzKucherenko":
        sensitivityAnalysis = ot.MauntzKucherenkoSensitivityAlgorithm(
            inputDesign, outputDesign, sample_size
        )
    else:
        raise ValueError("Unknown estimator %s" % (estimator))
    computed_first_order = sensitivityAnalysis.getFirstOrderIndices()
    computed_total_order = sensitivityAnalysis.getTotalOrderIndices()
    exact_first_order = problem.getFirstOrderIndices()
    exact_total_order = problem.getTotalOrderIndices()
    dimension = distribution.getDimension()
    first_order_AE = ot.Point(dimension)
    total_order_AE = ot.Point(dimension)
    for i in range(dimension):
        first_order_AE[i] = otb.ComputeAbsoluteError(
            exact_first_order[i], computed_first_order[i]
        )
        total_order_AE[i] = otb.ComputeAbsoluteError(
            exact_total_order[i], computed_total_order[i]
        )
    return first_order_AE, total_order_AE


def compute_Sobol_table(
    problem,
    numberOfExperiments=12,
    numberOfRepetitions=10,
    maximum_elapsed_time=2.0,
    sample_size_initial=20,
    estimator="Saltelli",
    verbose=False,
):
    """
    Repeat increasingly large Monte-Carlo Sobol' experiments.

    The goal of this function is to see how the Sobol' estimator
    converges when the sample size increases.
    For each sample size, we repeat the experiment a given number of
    times, in order to see the variability of the estimator.
    At each stage of the simulation, the sample size is multiplied by 2.
    The number of performed simulation depends on the maximum elapsed time:
    when this time exceeds a given duration, the algorithm stops.

    Parameters
    ----------
    problem : otbenchmark.SensitivityBenchmarkProblem
        The problem to solve.
    numberOfExperiments : int
        Number of atomic experiments, i.e. the number of times the sample
        size increases.
    numberOfRepetitions : int
        Number of repetions for a given sample size.
    maximum_elapsed_time : float
        The maximum number of seconds in the simulation.
    sample_size_initial : int
        The initial sample size.
    estimator : str
        The name of the estimator.
        Can be "Saltelli", "Martinez", "Jansen", "MauntzKucherenko".

    Returns
    -------
    sample_size_table : ot.Sample(number_of_performed_experiments, 1)
        The sample size of each experiment.
    first_order_table : ot.Sample(number_of_performed_experiments, dimension)
        The AE of the first order Sobol' indices.
    total_order_table : ot.Sample(number_of_performed_experiments, dimension)
        The AE of the total order Sobol' indices.
    """
    startTime = time.time()

    first_order_data = []
    total_order_data = []

    sample_size = sample_size_initial
    sample_size_data = []
    index = 0
    for i in range(numberOfExperiments):
        elapsedTime = time.time() - startTime
        if elapsedTime > maximum_elapsed_time:
            break
        sample_size *= 2
        if verbose:
            print("Elapsed = %.1f (s), Sample size = %d" % (elapsedTime, sample_size))
        for j in range(numberOfRepetitions):
            first_order_AE, total_order_AE = compute_AE_by_sampling(
                problem, sample_size, estimator=estimator
            )
            sample_size_data.append([sample_size])
            first_order_data.append(first_order_AE)
            total_order_data.append(total_order_AE)
            index += 1

    elapsedTime = time.time() - startTime
    if verbose:
        print("Elapsed = %.2f (s)" % (elapsedTime))

    # Create the `Sample` from the data.
    sample_size_table = ot.Sample(sample_size_data)
    first_order_table = ot.Sample(first_order_data)
    distribution = problem.getInputDistribution()
    dimension = distribution.getDimension()
    description = []
    for marginal_index in range(dimension):
        description.append("$S_%d$" % (marginal_index))
    first_order_table.setDescription(description)
    # Total order
    total_order_table = ot.Sample(total_order_data)
    description = []
    for marginal_index in range(dimension):
        description.append("$T_%d$" % (marginal_index))
    total_order_table.setDescription(description)
    return sample_size_table, first_order_table, total_order_table


def plot_Sobol_grid(
    problem,
    numberOfExperiments=12,
    numberOfRepetitions=10,
    maximum_elapsed_time=2.0,
    sample_size_initial=20,
    estimator="Saltelli",
    verbose=False,
):
    """
    Plot increasingly large Monte-Carlo Sobol' experiments.

    The goal of this function is to see how the Sobol' estimator
    converges when the sample size increases.
    For each sample size, we repeat the experiment a given number of
    times, in order to see the variability of the estimator.
    At each stage of the simulation, the sample size is multiplied by 2.
    The number of performed simulation depends on the maximum elapsed time:
    when this time exceeds a given duration, the algorithm stops.

    Parameters
    ----------
    problem : otbenchmark.SensitivityBenchmarkProblem
        The problem to solve.
    numberOfExperiments : int
        Number of atomic experiments, i.e. the number of times the sample
        size increases.
    numberOfRepetitions : int
        Number of repetions for a given sample size.
    maximum_elapsed_time : float
        The maximum number of seconds in the simulation.
    sample_size_initial : int
        The initial sample size.
    estimator : str
        The name of the estimator.
        Can be "Saltelli", "Martinez", "Jansen", "MauntzKucherenko".

    Returns
    -------
    grid : ot.GridLayout
        The grid of convergence Graphs.
    """
    sample_size_table, first_order_table, total_order_table = compute_Sobol_table(
        problem,
        numberOfExperiments=numberOfExperiments,
        numberOfRepetitions=numberOfRepetitions,
        maximum_elapsed_time=maximum_elapsed_time,
        sample_size_initial=sample_size_initial,
        estimator=estimator,
        verbose=verbose,
    )
    # Create a table for the reference Monte-Carlo convergence rate.
    sample_size_initial = np.min(sample_size_table)
    sample_size_final = np.max(sample_size_table)
    sample_size_log_array = np.logspace(
        np.log10(sample_size_initial), np.log10(sample_size_final)
    )
    sampleSizeArray = [int(n) for n in sample_size_log_array]
    expectedConvergence = [1.0 / np.sqrt(n) for n in sampleSizeArray]

    # Create plot
    distribution = problem.getInputDistribution()
    dimension = distribution.getDimension()
    grid = ot.GridLayout(2, dimension)
    for marginal_index in range(dimension):
        for first_order_sobol_estimator in [True, False]:
            # If first_order_sobol_estimator, then plot LRE of first order Sobol' index
            # otherwise, plot LRE of total order Sobol' index
            if first_order_sobol_estimator:
                label = "$S_%d$" % (marginal_index)
            else:
                label = "$T_%d$" % (marginal_index)
            title = ""
            graph = ot.Graph(
                title, "Sample size", "Absolute error of %s" % (label), True, "topright"
            )
            if first_order_sobol_estimator:
                cloud = ot.Cloud(
                    sample_size_table, first_order_table[:, marginal_index]
                )
            else:
                cloud = ot.Cloud(
                    sample_size_table, total_order_table[:, marginal_index]
                )
            cloud.setPointStyle("fsquare")
            cloud.setLegend("MC")
            graph.add(cloud)
            curve = ot.Curve(sampleSizeArray, expectedConvergence)
            curve.setLegend(r"$1/\sqrt{n}$")
            graph.add(curve)
            graph.setColors(ot.Drawable_BuildDefaultPalette(2))
            graph.setLogScale(ot.GraphImplementation.LOGXY)
            if first_order_sobol_estimator:
                row_index = 0
            else:
                row_index = 1
            graph.setLegendPosition("bottomleft")
            grid.setGraph(row_index, marginal_index, graph)
    return grid


def plot_Sobol_curve(
    problem,
    numberOfExperiments=12,
    numberOfRepetitions=10,
    maximum_elapsed_time=2.0,
    sample_size_initial=20,
    estimator="Saltelli",
    verbose=False,
):
    """
    Plot increasingly large Monte-Carlo Sobol' experiments.

    The goal of this function is to see how the Sobol' estimator
    converges when the sample size increases.
    For each sample size, we repeat the experiment a given number of
    times, in order to see the variability of the estimator.
    At each stage of the simulation, the sample size is multiplied by 2.
    The number of performed simulation depends on the maximum elapsed time:
    when this time exceeds a given duration, the algorithm stops.

    Parameters
    ----------
    problem : otbenchmark.SensitivityBenchmarkProblem
        The problem to solve.
    numberOfExperiments : int
        Number of atomic experiments, i.e. the number of times the sample
        size increases.
    numberOfRepetitions : int
        Number of repetions for a given sample size.
    maximum_elapsed_time : float
        The maximum number of seconds in the simulation.
    sample_size_initial : int
        The initial sample size.
    estimator : str
        The name of the estimator.
        Can be "Saltelli", "Martinez", "Jansen", "MauntzKucherenko".

    Returns
    -------
    sample_size_table : ot.Sample(number_of_performed_experiments, 1)
        The sample size of each experiment.
    first_order_table : ot.Sample(number_of_performed_experiments, dimension)
        The AE of the first order Sobol' indices.
    total_order_table : ot.Sample(number_of_performed_experiments, dimension)
        The AE of the total order Sobol' indices.
    """
    sample_size_table, first_order_table, total_order_table = compute_Sobol_table(
        problem,
        numberOfExperiments=numberOfExperiments,
        numberOfRepetitions=numberOfRepetitions,
        maximum_elapsed_time=maximum_elapsed_time,
        sample_size_initial=sample_size_initial,
        estimator=estimator,
        verbose=verbose,
    )
    # Create a table for the reference Monte-Carlo convergence rate.
    sample_size_initial = np.min(sample_size_table)
    sample_size_final = np.max(sample_size_table)
    sample_size_log_array = np.logspace(
        np.log10(sample_size_initial), np.log10(sample_size_final)
    )
    sampleSizeArray = [int(n) for n in sample_size_log_array]
    sampling_method = ot.ResourceMap.GetAsString(
        "SobolIndicesExperiment-SamplingMethod"
    )
    if sampling_method == "QMC":
        expectedConvergence = [1.0 / n for n in sampleSizeArray]
    else:
        expectedConvergence = [1.0 / np.sqrt(n) for n in sampleSizeArray]

    # Create plot
    title = "%s, %s" % (problem.getName(), estimator)
    graph = ot.Graph(title, "Sample size", "Absolute error", True, "topright")
    distribution = problem.getInputDistribution()
    dimension = distribution.getDimension()
    for marginal_index in range(dimension):
        for first_order_sobol_estimator in [True, False]:
            # If first_order_sobol_estimator, then plot LRE of first order Sobol' index
            # otherwise, plot LRE of total order Sobol' index
            if first_order_sobol_estimator:
                label = "$S_%d$" % (marginal_index)
            else:
                label = "$T_%d$" % (marginal_index)
            if first_order_sobol_estimator:
                cloud = ot.Cloud(
                    sample_size_table, first_order_table[:, marginal_index]
                )
            else:
                cloud = ot.Cloud(
                    sample_size_table, total_order_table[:, marginal_index]
                )
            cloud.setPointStyle("fsquare")
            cloud.setLegend(label)
            graph.add(cloud)
    curve = ot.Curve(sampleSizeArray, expectedConvergence)
    if sampling_method == "QMC":
        reference_legend = r"$1/n$"
    else:
        reference_legend = r"$1/\sqrt{n}$"
    curve.setLegend(reference_legend)
    graph.add(curve)
    graph.setColors(ot.Drawable_BuildDefaultPalette(2 + 2 * dimension))
    graph.setLogScale(ot.GraphImplementation.LOGXY)
    graph.setLegendPosition("bottomleft")
    return graph
