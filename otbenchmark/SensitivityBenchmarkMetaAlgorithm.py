# -*- coding: utf-8 -*-
"""
Manage sensitivity problems.
"""
import openturns as ot
import otbenchmark as otb


class SensitivityBenchmarkMetaAlgorithm:
    @staticmethod
    def GetEstimators():
        """
        Get the available sample-based estimators.

        This currently involves four estimators:
        * ot.SaltelliSensitivityAlgorithm
        * ot.MartinezSensitivityAlgorithm
        * ot.JansenSensitivityAlgorithm
        * ot.MauntzKucherenkoSensitivityAlgorithm

        Parameters
        ----------
        None.

        Returns
        -------
        estimators_list : list of ot.SobolIndicesAlgorithm
            The list of available sample-based Sobol' indices estimators.

        """
        estimators_list = [
            ot.SaltelliSensitivityAlgorithm(),
            ot.MartinezSensitivityAlgorithm(),
            ot.JansenSensitivityAlgorithm(),
            ot.MauntzKucherenkoSensitivityAlgorithm(),
        ]
        return estimators_list

    def __init__(self, problem):
        """
        Create a meta-algorithm to solve a sensitivity problem.


        Parameters
        ----------
        problem : ot.SensitivityBenchmarkProblem
            The problem.
        """
        #
        self.problem = problem
        return None

    def runSamplingEstimator(
        self, sobolIndicesAlgorithm, sample_size, sampling_method="MonteCarlo"
    ):
        """
        Runs the sampling sensitivity estimator and get the results.

        Uses a Monte-Carlo sample.

        Parameters
        ----------
        sobolIndicesAlgorithm : ot.SobolIndicesAlgorithm
            The estimator based on a Monte-Carlo sample.
        sample_size: int
            The sample size.
        sampling_method : str
            The sampling method.
            Must be "MonteCarlo" or "LHS" or "QMC".

        Returns
        -------
        first_order: ot.Point(dimension)
            The Sobol' first order indices.
        total_order: ot.Point(dimension)
            The Sobol' total order indices.
        """
        if (
            sampling_method == "MonteCarlo"
            or sampling_method == "LHS"
            or sampling_method == "QMC"
        ):
            ot.ResourceMap.SetAsString(
                "SobolIndicesExperiment-SamplingMethod", sampling_method
            )
        else:
            raise ValueError("Unknown value of %s" % (sampling_method))
        distribution = self.problem.getInputDistribution()
        model = self.problem.getFunction()
        inputDesign = ot.SobolIndicesExperiment(distribution, sample_size).generate()
        outputDesign = model(inputDesign)
        sobolIndicesAlgorithm.setDesign(inputDesign, outputDesign, sample_size)
        first_order = sobolIndicesAlgorithm.getFirstOrderIndices()
        total_order = sobolIndicesAlgorithm.getTotalOrderIndices()
        return first_order, total_order

    def runSamplingEstimatorB(
        self, sobolIndicesAlgorithm, sample_size, sampling_method="MonteCarlo"
    ):
        """
        Runs the sampling sensitivity estimator and get the results.

        Uses a Monte-Carlo sample.

        Parameters
        ----------
        sobolIndicesAlgorithm : ot.SobolIndicesAlgorithm
            The estimator based on a Monte-Carlo sample.
        sample_size: int
            The sample size.
        sampling_method : str
            The sampling method.
            Must be "MonteCarlo" or "LHS" or "QMC".

        Returns
        -------
        first_order: ot.Point(dimension)
            The Sobol' first order indices.
        total_order: ot.Point(dimension)
            The Sobol' total order indices.
        """
        if (
            sampling_method == "MonteCarlo"
            or sampling_method == "LHS"
            or sampling_method == "QMC"
        ):
            ot.ResourceMap.SetAsString(
                "SobolIndicesExperiment-SamplingMethod", sampling_method
            )
        else:
            raise ValueError("Unknown value of %s" % (sampling_method))
        distribution = self.problem.getInputDistribution()
        model = self.problem.getFunction()
        inputDesign = ot.SobolIndicesExperiment(distribution, sample_size).generate()
        outputDesign = model(inputDesign)
        sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(
            inputDesign, outputDesign, sample_size
        )
        first_order = sensitivityAnalysis.getFirstOrderIndices()
        total_order = sensitivityAnalysis.getTotalOrderIndices()
        return first_order, total_order

    def runPolynomialChaosEstimator(
        self,
        sample_size_train=100,
        sample_size_test=100,
        total_degree=2,
        hyperbolic_quasinorm=0.5,
    ):
        """
        Estimate Sobol' sensitivity indices from sparse polynomial chaos.

        Uses regression to estimate the coefficients.
        Uses LARS to select the model.
        Uses hyperbolic enumerate rule.
        Uses Sobol' low discrepancy sequence to train the polynomial.
        Uses Monte-Carlo sample to test the polynomial.

        Parameters
        ----------
        sample_size_train : int, optional
            The training sample size. The default is 100.
        sample_size_test : int, optional
            The test sample size. The default is 100.
        total_degree : int, optional
            The total polynomial degree. The default is 2.
        hyperbolic_quasinorm : float, optional
            The hyperbolic quasi-norm. The default is 0.5.

        Returns
        -------
        first_order: ot.Point(dimension)
            The Sobol' first order indices.
        total_order: ot.Point(dimension)
            The Sobol' total order indices.
        """
        sparse_sa = otb.SparsePolynomialChaosSensitivityAnalysis(
            self.problem,
            sample_size_train=sample_size_train,
            sample_size_test=sample_size_test,
            total_degree=total_degree,
            hyperbolic_quasinorm=hyperbolic_quasinorm,
        )
        result = sparse_sa.run()
        return result.first_order_indices, result.total_order_indices
