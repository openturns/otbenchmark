"""
Perform a convergence study of a sensitivity analysis estimator.
"""

import openturns as ot
import numpy as np
import time
import math


class SensitivityConvergence:
    def __init__(
        self,
        problem,
        metaSAAlgorithm,
        numberOfExperiments=1000,
        numberOfRepetitions=10,
        maximumElapsedTime=5.0,
        sampleSizeInitial=20,
        estimator="Saltelli",
        samplingMethod="MonteCarlo",
        useSampling=True,
        totalDegree=2,
        hyperbolicQuasiNorm=0.5,
        graphicalEpsilon=2 * ot.SpecFunc.ScalarEpsilon,
        sampleSizeFactor=2.0,
        sparse=True,
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
            Number of repetitions for a given sample size.
            The numberOfRepetitions attribute sets the number of vertical
            points in each graph.
        maximumElapsedTime : float
            The maximum number of seconds in the simulation.
        sampleSizeInitial : int
            The initial sample size.
        estimator : str
            The estimator.
            Must be "Saltelli", "Jansen", "Martinez", "MauntzKucherenko", "Janon".
        samplingMethod : str
            The sampling method.
            Must be "MonteCarlo" or "LHS" or "QMC".
        useSampling : bool
            Set to True to use sampling methods.
            Set to False to use polynomial chaos.
        totalDegree : int
            The total degree of the polynomial chaos.
        hyperbolicQuasiNorm : float
            The quasi-norm of the enumeration rule of the polynomial chaos.
        graphicalEpsilon : float
            The value which is set as the minimum absolute error of Sobol' indices.
            This allows to use logarithmic scale even if the absolute error is
            exactly zero.
        sampleSizeFactor : float
            The factor by which the sample size is multiplied at each stage of
            the simulation.
            The default is 2.0.
        sparse : bool, optional
            Whether to use sparse polynomial chaos. The default is True.
        """
        validSamplingMethods = {"MonteCarlo", "LHS", "QMC"}
        validEstimators = {
            "Saltelli",
            "Jansen",
            "Martinez",
            "MauntzKucherenko",
            "Janon",
        }

        if samplingMethod not in validSamplingMethods:
            raise ValueError(
                f"Unknown value of sampling method: {samplingMethod}. "
                f"Possible values are: {sorted(list(validSamplingMethods))}"
            )

        if estimator not in validEstimators:
            raise ValueError(
                f"Unknown value of estimator: {estimator}. "
                f"Possible values are: {sorted(list(validEstimators))}"
            )
        if sampleSizeFactor <= 1.0:
            raise ValueError(
                f"The sample size factor must be strictly larger than 1.0, but is {sampleSizeFactor}"
            )
        if numberOfExperiments <= 0:
            raise ValueError("numberOfExperiments must be strictly positive.")

        if numberOfRepetitions <= 0:
            raise ValueError("numberOfRepetitions must be strictly positive.")

        if maximumElapsedTime <= 0.0:
            raise ValueError("maximumElapsedTime must be strictly positive.")

        if sampleSizeInitial <= 0:
            raise ValueError("sampleSizeInitial must be strictly positive.")

        if totalDegree < 0:
            raise ValueError("totalDegree must be non-negative.")

        if not (0.0 < hyperbolicQuasiNorm <= 1.0):
            raise ValueError("hyperbolicQuasiNorm must be in the range (0, 1].")

        if graphicalEpsilon <= 0.0:
            raise ValueError("graphicalEpsilon must be strictly positive.")

        self.estimator = estimator
        self.problem = problem
        self.metaSAAlgorithm = metaSAAlgorithm
        self.numberOfExperiments = numberOfExperiments
        self.numberOfRepetitions = numberOfRepetitions
        self.maximumElapsedTime = maximumElapsedTime
        self.sampleSizeInitial = sampleSizeInitial
        self.samplingMethod = samplingMethod
        self.useSampling = useSampling
        self.totalDegree = totalDegree
        self.hyperbolicQuasiNorm = hyperbolicQuasiNorm
        self.graphicalEpsilon = graphicalEpsilon
        self.sampleSizeFactor = sampleSizeFactor
        self.sparse = sparse
        return None

    def computeError(self, sampleSize):
        r"""
        Compute the absolute error for the problem with Monte-Carlo sample.

        Uses Saltelli estimator.

        For some cases, the reference Sobol' index is zero.
        This is why the relative error cannot be used as a metric.
        We compute the absolute error between the reference Sobol'
        indices and the computed Sobol' indices:

        .. math::

            \text{AE}_i = \left|S_{\text{computed},i} - S_{\text{reference}, i}\right|

        for :math:`i \in \{1, ..., \inputDim\}` where :math:`\inputDim` is the
        dimension of the problem.

        Parameters
        ----------
        sampleSize: int
            The sample size.

        Returns
        -------
        firstOrderAE : ot.Point(dimension)
            The AE of the first order Sobol' indices.
        totalOrderAE : ot.Point(dimension)
            The AE of the total order Sobol' indices.
        """
        if self.useSampling:
            (
                computedFirstOrder,
                computedTotalOrder,
            ) = self.metaSAAlgorithm.runSamplingEstimator(
                sampleSize, self.estimator, self.samplingMethod
            )
        else:
            (
                computedFirstOrder,
                computedTotalOrder,
            ) = self.metaSAAlgorithm.runPolynomialChaosEstimator(
                sampleSizeTrain=sampleSize,
                sampleSizeTest=2,  # Bare minimum
                totalDegree=self.totalDegree,
                hyperbolicQuasiNorm=self.hyperbolicQuasiNorm,
                sparse=self.sparse,
            )
        exactFirstOrder = self.problem.getFirstOrderIndices()
        exactTotalOrder = self.problem.getTotalOrderIndices()
        firstOrderAE = ot.Point(np.abs(exactFirstOrder - computedFirstOrder))
        totalOrderAE = ot.Point(np.abs(exactTotalOrder - computedTotalOrder))
        # Set zero components to a minimum.
        # This allows to use a log-scale when the estimator is very accurate and
        # leads to a zero error.
        distribution = self.problem.getInputDistribution()
        dimension = distribution.getDimension()
        for i in range(dimension):
            firstOrderAE[i] = max(firstOrderAE[i], self.graphicalEpsilon)
            totalOrderAE[i] = max(totalOrderAE[i], self.graphicalEpsilon)
        return firstOrderAE, totalOrderAE

    def computeSobolSample(
        self,
        verbose=True,
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
        sampleSizeTable : ot.Sample(numberOfExperiments, 1)
            The sample size of each experiment.
        firstOrderTable : ot.Sample(numberOfExperiments, dimension)
            The AE of the first order Sobol' indices.
        totalOrderTable : ot.Sample(numberOfExperiments, dimension)
            The AE of the total order Sobol' indices.
        """
        startTime = time.time()

        sampleSize = self.sampleSizeInitial
        sampleSizeData = []
        firstOrderData = []
        totalOrderData = []
        for i in range(self.numberOfExperiments):
            elapsedTime = time.time() - startTime
            if elapsedTime > self.maximumElapsedTime:
                if verbose:
                    print(
                        f"Elapsed = {elapsedTime:.1f} (s) > {self.maximumElapsedTime:.1f} (s),"
                        " stopping the simulation."
                    )
                break
            if verbose:
                print(f"Elapsed = {elapsedTime:.1f} (s), Sample size = {sampleSize}")
            for j in range(self.numberOfRepetitions):
                try:
                    firstOrderAE, totalOrderAE = self.computeError(
                        sampleSize,
                    )
                except Exception as e:
                    if verbose:
                        print(
                            f"Error in experiment {i}, repetition {j}, sample size {sampleSize}: {e}"
                        )
                    continue
                sampleSizeData.append([sampleSize])
                firstOrderData.append(firstOrderAE)
                totalOrderData.append(totalOrderAE)

            sampleSize = max(
                sampleSize + 1,
                math.ceil(sampleSize * self.sampleSizeFactor),
            )

        elapsedTime = time.time() - startTime
        if verbose:
            print(f"Elapsed = {elapsedTime:.2f} (s)")

        # Create the `Sample` from the data.
        sampleSizeTable = ot.Sample(sampleSizeData)
        firstOrderTable = ot.Sample(firstOrderData)
        totalOrderTable = ot.Sample(totalOrderData)
        return sampleSizeTable, firstOrderTable, totalOrderTable

    def _getConvergenceData(self, verbose=False):
        """
        Private method to get the data for the convergence curve.
        """
        # Exécution des simulations
        sampleSizeTable, firstOrderTable, totalOrderTable = self.computeSobolSample(
            verbose=verbose
        )

        # Calcul des échelles logarithmiques pour la courbe de référence
        sampleSizeInitial = sampleSizeTable.getMin()[0]
        sampleSizeFinal = sampleSizeTable.getMax()[0]
        sampleSizeLogArray = np.logspace(
            np.log10(sampleSizeInitial), np.log10(sampleSizeFinal)
        )
        sampleSizeArray = [int(n) for n in sampleSizeLogArray]

        # Calcul de la convergence théorique attendue
        if self.useSampling and self.samplingMethod == "QMC":
            expectedConvergence = [1.0 / n for n in sampleSizeArray]
            referenceLegend = r"$1/n$"
        else:
            expectedConvergence = [1.0 / np.sqrt(n) for n in sampleSizeArray]
            referenceLegend = r"$1/\sqrt{n}$"

        return (
            sampleSizeTable,
            firstOrderTable,
            totalOrderTable,
            sampleSizeArray,
            expectedConvergence,
            referenceLegend,
        )

    def plotConvergenceGrid(
        self,
        verbose=False,
    ):
        """
        Plot increasingly large Monte-Carlo Sobol' experiments.

        The goal of this function is to see how the Sobol' estimator
        converges when the sample size increases.
        See computeSobolSample for more details.

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
            sampleSizeTable,
            firstOrderTable,
            totalOrderTable,
            sampleSizeArray,
            expectedConvergence,
            referenceLegend,
        ) = self._getConvergenceData(verbose=verbose)

        # Create plot
        distribution = self.problem.getInputDistribution()
        dimension = distribution.getDimension()
        grid = ot.GridLayout(2, dimension)
        for marginalIndex in range(dimension):
            for firstOrderSobolEstimator in [True, False]:
                # If firstOrderSobolEstimator, then plot absolute error of first order
                # Sobol' index,
                # otherwise, plot absolute error of total order Sobol' index.
                if firstOrderSobolEstimator:
                    label = f"$S_{marginalIndex}$"
                else:
                    label = f"$T_{marginalIndex}$"
                title = ""
                graph = ot.Graph(
                    title,
                    "Sample size",
                    f"Absolute error of {label}",
                    True,
                    "topright",
                )
                if firstOrderSobolEstimator:
                    cloud = ot.Cloud(sampleSizeTable, firstOrderTable[:, marginalIndex])
                else:
                    cloud = ot.Cloud(sampleSizeTable, totalOrderTable[:, marginalIndex])
                cloud.setPointStyle("fsquare")
                cloud.setLegend("MC")
                graph.add(cloud)
                curve = ot.Curve(sampleSizeArray, expectedConvergence)
                curve.setLegend(r"$1/\sqrt{n}$")
                graph.add(curve)
                graph.setColors(ot.Drawable.BuildDefaultPalette(2))
                graph.setLogScale(ot.GraphImplementation.LOGXY)
                if firstOrderSobolEstimator:
                    rowIndex = 0
                else:
                    rowIndex = 1
                graph.setLegendPosition("bottomleft")
                grid.setGraph(rowIndex, marginalIndex, graph)
        return grid

    def plotConvergenceCurve(
        self,
        verbose=False,
    ):
        """
        Plot increasingly large Monte-Carlo Sobol' experiments.

        The goal of this function is to see how the Sobol' estimator
        converges when the sample size increases.
        See computeSobolSample for more details.

        Parameters
        ----------
        verbose : bool
            If True, then prints intermediate messages.

        Returns
        -------
        graph : ot.Graph
            The convergence Graph.
        """
        (
            sampleSizeTable,
            firstOrderTable,
            totalOrderTable,
            sampleSizeArray,
            expectedConvergence,
            referenceLegend,
        ) = self._getConvergenceData(verbose=verbose)

        # Create plot
        if self.useSampling:
            title = f"{self.problem.getName()}, {self.estimator}, {self.samplingMethod}"
        else:
            title = f"{self.problem.getName()}, P.C., Degree={self.totalDegree}"
        graph = ot.Graph(title, "Sample size", "Absolute error", True, "topright")
        distribution = self.problem.getInputDistribution()
        dimension = distribution.getDimension()
        # Plot absolute error
        for marginalIndex in range(dimension):
            for firstOrderSobolEstimator in [True, False]:
                if firstOrderSobolEstimator:
                    label = f"$S_{{{marginalIndex}}}$"
                else:
                    label = f"$T_{{{marginalIndex}}}$"
                if firstOrderSobolEstimator:
                    cloud = ot.Cloud(sampleSizeTable, firstOrderTable[:, marginalIndex])
                else:
                    cloud = ot.Cloud(sampleSizeTable, totalOrderTable[:, marginalIndex])
                cloud.setPointStyle("fsquare")
                cloud.setLegend(label)
                graph.add(cloud)
        # Plot expected convergence rate
        if self.useSampling:
            curve = ot.Curve(sampleSizeArray, expectedConvergence)
            curve.setLegend(referenceLegend)
            graph.add(curve)
        graph.setLogScale(ot.GraphImplementation.LOGXY)
        graph.setLegendPosition("topright")
        graph.setColors(ot.Drawable.BuildDefaultPalette(2 + 2 * dimension))
        return graph
