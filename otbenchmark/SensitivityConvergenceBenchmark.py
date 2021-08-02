#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 16:55:05 2021

@author: devel
"""
import openturns as ot
import otbenchmark as otb
import numpy as np
import time


class SensitivityConvergenceBenchmark:
    def __init__(
        self,
        problem,
        metaSAAlgorithm,
        numberOfExperiments=12,
        numberOfRepetitions=10,
        maximum_elapsed_time=5.0,
        sample_size_initial=20,
    ):
        """
        Create a meta-algorithm to benchmark a sensitivity problem.

        Parameters
        ----------
        problem : ot.SensitivityBenchmarkProblem
            The problem.
        metaSAAlgorithm : SensitivityBenchmarkMetaAlgorithm
            A meta-sensitivity algorithm.
        numberOfExperiments : int
            Number of atomic experiments, i.e. the number of times the sample
            size increases.
        numberOfRepetitions : int
            Number of repetions for a given sample size.
        maximum_elapsed_time : float
            The maximum number of seconds in the simulation.
        sample_size_initial : int
            The initial sample size.
        """
        #
        self.problem = problem
        self.metaSAAlgorithm = metaSAAlgorithm
        self.numberOfExperiments = numberOfExperiments
        self.numberOfRepetitions = numberOfRepetitions
        self.maximum_elapsed_time = maximum_elapsed_time
        self.sample_size_initial = sample_size_initial
        return None

    def computeError(self, sobolIndicesAlgorithm, sample_size):
        """
        Compute the absolute error for the problem with Monte-Carlo sample.

        Uses Saltelli estimator.

        For some cases, the reference Sobol' index is zero.
        This is why the relative error cannot be used as a metric.
        We compute the absolute error between the reference Sobol'
        indices and the computed Sobol' indices:

            AE(i) = abs(S_computed(i) - S_reference(i))

        for i = 1, ..., p where p is the dimension of the problem.

        Parameters
        ----------
        sobolIndicesAlgorithm : ot.SobolIndicesAlgorithm
            The estimator based on a Monte-Carlo sample.
        sample_size: int
            The sample size.

        Returns
        -------
        first_order_AE : ot.Point(dimension)
            The AE of the first order Sobol' indices.
        total_order_AE : ot.Point(dimension)
            The AE of the total order Sobol' indices.
        """
        print("sample_size=", sample_size)
        distribution = self.problem.getInputDistribution()
        dimension = distribution.getDimension()
        if True:
            (
                computed_first_order,
                computed_total_order,
            ) = self.metaSAAlgorithm.runSamplingEstimator(
                sobolIndicesAlgorithm, sample_size
            )
        else:
            (
                computed_first_order,
                computed_total_order,
            ) = self.metaSAAlgorithm.runSamplingEstimatorB(
                sobolIndicesAlgorithm, sample_size
            )

        exact_first_order = self.problem.getFirstOrderIndices()
        exact_total_order = self.problem.getTotalOrderIndices()
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

    def computeSobolSample(
        self, sobolIndicesAlgorithm, verbose=False,
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
        sobolIndicesAlgorithm : ot.SobolIndicesAlgorithm
            The estimator based on a Monte-Carlo sample.

        Returns
        -------
        sample_size_table : ot.Sample(number_of_experiments, 1)
            The sample size of each experiment.
        first_order_table : ot.Sample(number_of_experiments, dimension)
            The AE of the first order Sobol' indices.
        total_order_table : ot.Sample(number_of_experiments, dimension)
            The AE of the total order Sobol' indices.
        """
        startTime = time.time()

        sample_size = self.sample_size_initial
        sample_size_data = []
        first_order_data = []
        total_order_data = []
        for i in range(self.numberOfExperiments):
            elapsedTime = time.time() - startTime
            if elapsedTime > self.maximum_elapsed_time:
                break
            sample_size *= 2
            if verbose:
                print(
                    "Elapsed = %.1f (s), Sample size = %d" % (elapsedTime, sample_size)
                )
            for j in range(self.numberOfRepetitions):
                first_order_AE, total_order_AE = self.computeError(
                    sobolIndicesAlgorithm, sample_size,
                )
                sample_size_data.append([sample_size])
                first_order_data.append(first_order_AE)
                total_order_data.append(total_order_AE)
                print(sample_size, first_order_AE, total_order_AE)

        elapsedTime = time.time() - startTime
        if verbose:
            print("Elapsed = %.2f (s)" % (elapsedTime))

        # Create the `Sample` from the data.
        sample_size_table = ot.Sample(sample_size_data)
        first_order_table = ot.Sample(first_order_data)
        total_order_table = ot.Sample(total_order_data)
        return sample_size_table, first_order_table, total_order_table

    def plotConvergenceGrid(
        self, sobolIndicesAlgorithm, verbose=False,
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
        sobolIndicesAlgorithm : ot.SobolIndicesAlgorithm
            The estimator based on a Monte-Carlo sample.
        verbose : bool
            If True, then prints intermediate messages.

        Returns
        -------
        grid : ot.GridLayout
            The grid of convergence Graphs.
        """
        (
            sample_size_table,
            first_order_table,
            total_order_table,
        ) = self.computeSobolSample(sobolIndicesAlgorithm, verbose=verbose,)
        # Create a table for the reference Monte-Carlo convergence rate.
        sample_size_initial = np.min(sample_size_table)
        sample_size_final = np.max(sample_size_table)
        sample_size_log_array = np.logspace(
            np.log10(sample_size_initial), np.log10(sample_size_final)
        )
        sampleSizeArray = [int(n) for n in sample_size_log_array]
        expectedConvergence = [1.0 / np.sqrt(n) for n in sampleSizeArray]

        # Create plot
        distribution = self.problem.getInputDistribution()
        dimension = distribution.getDimension()
        grid = ot.GridLayout(2, dimension)
        for marginal_index in range(dimension):
            for first_order_sobol_estimator in [True, False]:
                # If first_order_sobol_estimator, then plot LRE of first order
                # Sobol' index,
                # otherwise, plot LRE of total order Sobol' index
                if first_order_sobol_estimator:
                    label = "$S_%d$" % (marginal_index)
                else:
                    label = "$T_%d$" % (marginal_index)
                title = ""
                graph = ot.Graph(
                    title,
                    "Sample size",
                    "Absolute error of %s" % (label),
                    True,
                    "topright",
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

    def plotConvergenceCurve(
        self, sobolIndicesAlgorithm, verbose=False,
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
        sobolIndicesAlgorithm : ot.SobolIndicesAlgorithm
            The estimator based on a Monte-Carlo sample.
                verbose : bool
            If True, then prints intermediate messages.

        Returns
        -------
        sample_size_table : ot.Sample(number_of_experiments, 1)
            The sample size of each experiment.
        first_order_table : ot.Sample(number_of_experiments, dimension)
            The AE of the first order Sobol' indices.
        total_order_table : ot.Sample(number_of_experiments, dimension)
            The AE of the total order Sobol' indices.
        """
        (
            sample_size_table,
            first_order_table,
            total_order_table,
        ) = self.computeSobolSample(verbose=verbose,)
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
        estimatorName = sobolIndicesAlgorithm.getClassName()
        title = "%s, %s" % (self.problem.getName(), estimatorName)
        graph = ot.Graph(title, "Sample size", "Absolute error", True, "topright")
        distribution = self.problem.getInputDistribution()
        dimension = distribution.getDimension()
        for marginal_index in range(dimension):
            for first_order_sobol_estimator in [True, False]:
                # If first_order_sobol_estimator, then plot LRE of first order
                # Sobol' index,
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
