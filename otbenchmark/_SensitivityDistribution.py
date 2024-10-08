"""
Analyses the distribution of Sobol' indices.
"""

import openturns as ot


class SensitivityDistribution:
    """
    Checks the distribution of the sensitivity indices estimators.

    We comapre the asymptotic distribution with an empirical sample of Sobol'
    indices estimates.

    We want to check that the distribution computed by the library is OK.
    When we estimate this distribution depending on the asymptotic estimator,
    this distribution is Gaussian.
    Otherwise, it is computed using kernel smoothing based on bootstrap.
    A first significant point is the mean of the distribution.
    The second significant point is the variance of the distribution, which
    is computed using the Delta-method when the asymptotic distribution is
    used.

    The reference distribution is computed based on a sample of Sobol' indices,
    which is generated by repetition.
    Then we compare the "Sample" distribution (from repetition) and the
    "Computed" distribution from the library.
    These two distributions should be close.
    """

    def __init__(
        self,
        problem,
        metaSAAlgorithm,
        sampleSize,
        numberOfRepetitions=10,
        estimator="Saltelli",
        sampling_method="MonteCarlo",
    ):
        """
        Checks the distribution of the Sobol' estimator.

        Parameters
        ----------
        problem : ot.SensitivityBenchmarkProblem
            The problem.
        metaSAAlgorithm : SensitivityBenchmarkMetaAlgorithm
            A meta-sensitivity algorithm.
        sampleSize : int, optional
            The sample size.
        numberOfRepetitions : int, optional
            The number of times the estimation is repeated. The default is 10.
        estimator : str
            The estimator.
            Must be "Saltelli", "Jansen", "Martinez", "MauntzKucherenko".
        sampling_method : str
            The sampling method.
            Must be "MonteCarlo" or "LHS" or "QMC".

        Returns
        -------
        None.

        """

        self.problem = problem
        self.metaSAAlgorithm = metaSAAlgorithm
        self.sampleSize = sampleSize
        self.numberOfRepetitions = numberOfRepetitions
        if (
            estimator != "Saltelli"
            and estimator != "Jansen"
            and estimator != "Martinez"
            and estimator != "MauntzKucherenko"
        ):
            raise ValueError("Unknown value of estimator %s" % (estimator))
        self.estimator = estimator
        if (
            sampling_method != "MonteCarlo"
            and sampling_method != "LHS"
            and sampling_method != "QMC"
        ):
            raise ValueError(
                "Unknown value of sampling method : %s" % (sampling_method)
            )
        self.sampling_method = sampling_method

    def compute_sample_indices(self):
        """
        Generate a sample of first order and total order Sobol' indices.

        Returns
        -------
        sampleFirst : ot.Sample(numberOfRepetitions, dimension)
            A sample of first order Sobol' indices.
        sampleTotal : TYPE
            A sample of total order Sobol' indices.
        distributionFirst : ot.Distribution
            The distribution of the first order Sobol' indices..
        distributionTotal : TYPE
            The distribution of the total order Sobol' indices..
        """

        distribution = self.problem.getInputDistribution()
        dimension = distribution.getDimension()
        model = self.problem.getFunction()
        sampleFirst = ot.Sample(self.numberOfRepetitions, dimension)
        sampleTotal = ot.Sample(self.numberOfRepetitions, dimension)

        experiment = ot.SobolIndicesExperiment(distribution, self.sampleSize)

        # loi asymptotique
        is_first_simulation = True

        for i in range(self.numberOfRepetitions):
            if (
                self.sampling_method == "MonteCarlo"
                or self.sampling_method == "LHS"
                or self.sampling_method == "QMC"
            ):
                ot.ResourceMap.SetAsString(
                    "SobolIndicesExperiment-SamplingMethod", self.sampling_method
                )
            else:
                raise ValueError(
                    "Unknown value of sampling method : %s" % (self.sampling_method)
                )
            inputDesign = experiment.generate()
            outputDesign = model(inputDesign)
            if self.estimator == "Saltelli":
                sobolAlgorithm = ot.SaltelliSensitivityAlgorithm()
            elif self.estimator == "Jansen":
                sobolAlgorithm = ot.JansenSensitivityAlgorithm()
            elif self.estimator == "Martinez":
                sobolAlgorithm = ot.MartinezSensitivityAlgorithm()
            elif self.estimator == "MauntzKucherenko":
                sobolAlgorithm = ot.MauntzKucherenkoSensitivityAlgorithm()
            else:
                raise ValueError("Unknown value of estimator %s" % (self.estimator))
            sobolAlgorithm.setDesign(inputDesign, outputDesign, self.sampleSize)
            first_order = sobolAlgorithm.getFirstOrderIndices()
            total_order = sobolAlgorithm.getTotalOrderIndices()
            sampleFirst[i] = first_order
            sampleTotal[i] = total_order

            # Get the distribution
            if is_first_simulation:
                distributionFirst = sobolAlgorithm.getFirstOrderIndicesDistribution()
                distributionTotal = sobolAlgorithm.getTotalOrderIndicesDistribution()
                is_first_simulation = False

        return (
            sampleFirst,
            sampleTotal,
            distributionFirst,
            distributionTotal,
        )

    def draw(
        self,
        mean_distribution=False,
    ):
        """
        Plot the distribution of the estimator and the distribution of the indices.

        Parameters
        ----------
        mean_distribution : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        """
        (
            sampleFirst,
            sampleTotal,
            distributionFirst,
            distributionTotal,
        ) = self.compute_sample_indices()
        distribution = self.problem.getInputDistribution()
        dimension = distribution.getDimension()
        grid = ot.GridLayout(2, dimension)
        exact_first_order = self.problem.getFirstOrderIndices()
        exact_total_order = self.problem.getTotalOrderIndices()

        # For each estimator, compare the distribution and the sample distribution
        for marginal_index in range(dimension):
            for first_order_sobol_estimator in [True, False]:
                if first_order_sobol_estimator:
                    label = "$S_{%d}$" % (marginal_index)
                else:
                    label = "$T_{%d}$" % (marginal_index)
                graph = ot.Graph("", label, "PDF", True, "topright")
                # Distribution of estimator
                if first_order_sobol_estimator:
                    sampleJ = sampleFirst[:, marginal_index]
                else:
                    sampleJ = sampleTotal[:, marginal_index]
                sampleDistribution = ot.KernelSmoothing().build(sampleJ)
                curve = sampleDistribution.drawPDF()
                curve.setLegends(["Sample"])
                graph.add(curve)
                # Distribution computed by estimator
                if first_order_sobol_estimator:
                    marginalDistribution = distributionFirst.getMarginal(marginal_index)
                else:
                    marginalDistribution = distributionTotal.getMarginal(marginal_index)
                curve = marginalDistribution.drawPDF()
                curve.setLegends(["Computed"])
                graph.add(curve)
                # Plot exact Sobol' index on the X axis
                if first_order_sobol_estimator:
                    data = exact_first_order[marginal_index]
                else:
                    data = exact_total_order[marginal_index]
                cloud = ot.Cloud([[data]], [[0.0]])
                cloud.setLegend("Exact")
                graph.add(cloud)
                # Graphics options
                graph.setColors(ot.DrawableImplementation.BuildDefaultPalette(3))
                if first_order_sobol_estimator:
                    row_index = 0
                else:
                    row_index = 1
                grid.setGraph(row_index, marginal_index, graph)
        return grid
