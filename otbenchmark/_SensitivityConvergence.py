#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Perform a convergence study of a sensitivity analysis estimator.
"""
import openturns as ot
import numpy as np
import time


class SensitivityConvergence:
    def __init__(
        self,
        problem,
        metaSAAlgorithm,
        numberOfExperiments=1000,
        numberOfRepetitions=10,
        maximum_elapsed_time=5.0,
        sample_size_initial=20,
        estimator="Saltelli",
        sampling_method="MonteCarlo",
        use_sampling=True,
        total_degree=2,
        hyperbolic_quasinorm=0.5,
        graphical_epsilon=2 * ot.SpecFunc.ScalarEpsilon,
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
            The default is set to a very large value, so that the algorithm
            stops depending on the elapsed time criteria.
        numberOfRepetitions : int
            Number of repetions for a given sample size.
            The numberOfRepetitions attribute sets the number of vertical
            points in each graph.
        maximum_elapsed_time : float
            The maximum number of seconds in the simulation.
        sample_size_initial : int
            The initial sample size.
        estimator : str
            The estimator.
            Must be "Saltelli", "Jansen", "Martinez", "MauntzKucherenko", "Janon".
        sampling_method : str
            The sampling method.
            Must be "MonteCarlo" or "LHS" or "QMC".
        use_sampling : bool
            Set to True to use sampling methods.
            Set to False to use polynomial chaos.
        total_degree : int
            The total degree of the polynomial chaos.
        hyperbolic_quasinorm : float
            The quasi-norm of the enumeration rule of the polynomial chaos.
        graphical_epsilon : float
            The value which is set as the minimum absolute error of Sobol' indices.
            This allows to use logarithmic scale even if the absolute error is
            exactly zero.
        """
        #
        self.problem = problem
        self.metaSAAlgorithm = metaSAAlgorithm
        self.numberOfExperiments = numberOfExperiments
        self.numberOfRepetitions = numberOfRepetitions
        self.maximum_elapsed_time = maximum_elapsed_time
        self.sample_size_initial = sample_size_initial
        if (
            sampling_method != "MonteCarlo"
            and sampling_method != "LHS"
            and sampling_method != "QMC"
        ):
            raise ValueError(
                "Unknown value of sampling method : %s" % (sampling_method)
            )
        self.sampling_method = sampling_method
        if (
            estimator != "Saltelli"
            and estimator != "Jansen"
            and estimator != "Martinez"
            and estimator != "MauntzKucherenko"
            and estimator != "Janon"
        ):
            raise ValueError("Unknown value of estimator %s" % (estimator))
        self.estimator = estimator
        self.use_sampling = use_sampling
        self.total_degree = total_degree
        self.hyperbolic_quasinorm = hyperbolic_quasinorm
        self.graphical_epsilon = graphical_epsilon
        return None

    def computeError(self, sample_size):
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
        sample_size: int
            The sample size.

        Returns
        -------
        first_order_AE : ot.Point(dimension)
            The AE of the first order Sobol' indices.
        total_order_AE : ot.Point(dimension)
            The AE of the total order Sobol' indices.
        """
        if self.use_sampling:
            (
                computed_first_order,
                computed_total_order,
            ) = self.metaSAAlgorithm.runSamplingEstimator(
                sample_size, self.estimator, self.sampling_method
            )
        else:
            (
                computed_first_order,
                computed_total_order,
            ) = self.metaSAAlgorithm.runPolynomialChaosEstimator(
                sample_size_train=sample_size,
                sample_size_test=2,  # Bare minimum
                total_degree=self.total_degree,
                hyperbolic_quasinorm=self.hyperbolic_quasinorm,
            )
        exact_first_order = self.problem.getFirstOrderIndices()
        exact_total_order = self.problem.getTotalOrderIndices()
        first_order_AE = ot.Point(np.abs(exact_first_order - computed_first_order))
        total_order_AE = ot.Point(np.abs(exact_total_order - computed_total_order))
        # Set zero components to a minimum.
        # This allows to use a log-scale when the estimator is very accurate and
        # leads to a zero error.
        distribution = self.problem.getInputDistribution()
        dimension = distribution.getDimension()
        for i in range(dimension):
            first_order_AE[i] = max(first_order_AE[i], self.graphical_epsilon)
            total_order_AE[i] = max(total_order_AE[i], self.graphical_epsilon)
        return first_order_AE, total_order_AE

    def computeSobolSample(
        self,
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
        verbose : bool
            Set to True to print intermediate messages.

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
                    sample_size,
                )
                sample_size_data.append([sample_size])
                first_order_data.append(first_order_AE)
                total_order_data.append(total_order_AE)

        elapsedTime = time.time() - startTime
        if verbose:
            print("Elapsed = %.2f (s)" % (elapsedTime))

        # Create the `Sample` from the data.
        sample_size_table = ot.Sample(sample_size_data)
        first_order_table = ot.Sample(first_order_data)
        total_order_table = ot.Sample(total_order_data)
        return sample_size_table, first_order_table, total_order_table

    def plotConvergenceGrid(
        self,
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
        ) = self.computeSobolSample(
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
        distribution = self.problem.getInputDistribution()
        dimension = distribution.getDimension()
        grid = ot.GridLayout(2, dimension)
        for marginal_index in range(dimension):
            for first_order_sobol_estimator in [True, False]:
                # If first_order_sobol_estimator, then plot asolute error of first order
                # Sobol' index,
                # otherwise, plot asolute error of total order Sobol' index.
                if first_order_sobol_estimator:
                    label = "$S_{%d}$" % (marginal_index)
                else:
                    label = "$T_{%d}$" % (marginal_index)
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
                graph.setColors(ot.Drawable.BuildDefaultPalette(2))
                graph.setLogScale(ot.GraphImplementation.LOGXY)
                if first_order_sobol_estimator:
                    row_index = 0
                else:
                    row_index = 1
                graph.setLegendPosition("bottomleft")
                grid.setGraph(row_index, marginal_index, graph)
        return grid

    def plotConvergenceCurve(
        self,
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
        ) = self.computeSobolSample(
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

        # Create plot
        if self.use_sampling:
            title = "%s, %s, %s" % (
                self.problem.getName(),
                self.estimator,
                self.sampling_method,
            )
        else:
            title = "%s, P.C., Degree=%d" % (self.problem.getName(), self.total_degree)
        graph = ot.Graph(title, "Sample size", "Absolute error", True, "topright")
        distribution = self.problem.getInputDistribution()
        dimension = distribution.getDimension()
        # Plot absolute error
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
        # Plot expected convergence rate
        if self.use_sampling:
            if sampling_method == "QMC":
                expectedConvergence = [1.0 / n for n in sampleSizeArray]
            else:
                expectedConvergence = [1.0 / np.sqrt(n) for n in sampleSizeArray]
            curve = ot.Curve(sampleSizeArray, expectedConvergence)
            if sampling_method == "QMC":
                reference_legend = r"$1/n$"
            else:
                reference_legend = r"$1/\sqrt{n}$"
            curve.setLegend(reference_legend)
            graph.add(curve)
        graph.setLogScale(ot.GraphImplementation.LOGXY)
        graph.setLegendPosition("topright")
        graph.setColors(ot.Drawable.BuildDefaultPalette(2 + 2 * dimension))
        return graph
