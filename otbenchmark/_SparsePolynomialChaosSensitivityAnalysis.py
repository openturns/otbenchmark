"""
Estimate sensitivity indices from sparse polynomial chaos
with hyperbolic enumerate function and regression.
"""

import openturns as ot


class SparsePolynomialChaosSensitivityResult:
    def __init__(
        self, predictivity_coefficient, first_order_indices, total_order_indices
    ):
        """
        The result of the sensitivity analysis from polynomial chaos.

        Parameters
        ----------
        predictivity_coefficient : float
            The predictivity coefficient. Always lower or equal to 1.
            Close to 1 is better.
            Lower than 0.5 means that the polynomial chaos metamodel
            cannot be trusted.
        first_order_indices : ot.Point(d)
            The first order sensitivity indices.
        total_order_indices : ot.Point(d)
            The total order sensitivity indices.

        Returns
        -------
        None.

        """
        self.predictivity_coefficient = predictivity_coefficient
        self.first_order_indices = first_order_indices
        self.total_order_indices = total_order_indices


class SparsePolynomialChaosSensitivityAnalysis:
    def __init__(
        self,
        sensitivityBenchmarkProblem,
        sample_size_train=100,
        sample_size_test=100,
        total_degree=2,
        hyperbolic_quasinorm=0.5,
        sparse=True,
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
        sensitivityBenchmarkProblem : otb.SensitivityBenchmarkProblem
            The problem.
        sample_size_train : int, optional
            The training sample size. The default is 100.
        sample_size_test : int, optional
            The test sample size. The default is 100.
        total_degree : int, optional
            The total polynomial degree. The default is 2.
        hyperbolic_quasinorm : float, optional
            The hyperbolic quasi-norm. The default is 0.5.
        sparse : bool, optional
            Set to True to compute a sparse PCE.
            Set to False to compute all coefficients.
            Default is True.

        Returns
        -------
        None.

        """
        self.problem = sensitivityBenchmarkProblem
        self.sample_size_train = sample_size_train
        self.sample_size_test = sample_size_test
        self.total_degree = total_degree
        self.hyperbolic_quasinorm = hyperbolic_quasinorm
        self.sparse = sparse

    def run(self, verbose=False):
        """
        Estimate the sensitivity indices from chaos.

        Parameters
        ----------
        verbose : bool, optional
            If True, print intermediate messages. The default is False.

        Returns
        -------
        result : otb.SparsePolynomialChaosSensitivityResult
            The result of the calculation.

        """
        distribution = self.problem.getInputDistribution()
        model = self.problem.getFunction()
        dimension = distribution.getDimension()
        if verbose:
            print(f"Generate train experiment, N={self.sample_size_train}")
        sequence = ot.SobolSequence(dimension)
        experiment = ot.LowDiscrepancyExperiment(
            sequence, distribution, self.sample_size_train
        )
        inputTrain = experiment.generate()
        outputTrain = model(inputTrain)

        # Create polynomial chaos expansion
        if verbose:
            print("Create polynomial chaos expansion..")
        distributionList = [distribution.getMarginal(i) for i in range(dimension)]
        multivariateBasis = ot.OrthogonalProductPolynomialFactory(distributionList)
        if self.sparse:
            selectionAlgorithm = ot.LeastSquaresMetaModelSelectionFactory()
        else:
            selectionAlgorithm = ot.PenalizedLeastSquaresAlgorithmFactory()
        projectionStrategy = ot.LeastSquaresStrategy(
            inputTrain, outputTrain, selectionAlgorithm
        )

        polyColl = [
            ot.StandardDistributionPolynomialFactory(distributionList[i])
            for i in range(dimension)
        ]
        enumerateFunction = ot.HyperbolicAnisotropicEnumerateFunction(
            dimension, self.hyperbolic_quasinorm
        )
        multivariateBasis = ot.OrthogonalProductPolynomialFactory(
            polyColl, enumerateFunction
        )

        enumfunc = multivariateBasis.getEnumerateFunction()
        basis_dimension = enumfunc.getBasisSizeFromTotalDegree(self.total_degree)
        if verbose:
            print(f"> Sparse = {self.sparse}")
            print(f"> Total degree = {self.total_degree}")
            print(f"> Basis dimension = {basis_dimension}")
            if basis_dimension >= self.sample_size_train:
                raise ValueError(
                    f"The number of candidate coefficients is {basis_dimension} "
                    f"is larger or equal to the sample size {self.sample_size_train}"
                )
        adaptiveStrategy = ot.FixedStrategy(multivariateBasis, basis_dimension)
        chaosalgo = ot.FunctionalChaosAlgorithm(
            inputTrain, outputTrain, distribution, adaptiveStrategy, projectionStrategy
        )
        if verbose:
            print("> Fit")
        chaosalgo.run()
        chaosResult = chaosalgo.getResult()
        number_of_coefficients = chaosResult.getCoefficients().getSize()
        if verbose:
            print(f"> Number of selected coefficients: {number_of_coefficients}")

        # Validation
        if verbose:
            print("> Validation...")
            print(f"> Generate test experiment, N={self.sample_size_test}")
        metamodel = chaosResult.getMetaModel()  # get the metamodel
        experiment = ot.MonteCarloExperiment(distribution, self.sample_size_test)
        inputTest = experiment.generate()
        outputTest = model(inputTest)
        predictions = metamodel(inputTest)
        val = ot.MetaModelValidation(outputTest, predictions)
        predictivity_coefficient = val.computeR2Score()[0]
        if verbose:
            print(f"> Q2={100 * predictivity_coefficient:0.2f}%")

        # S.A.
        if verbose:
            print("> Sensitivity Analysis...")
        chaosSI = ot.FunctionalChaosSobolIndices(chaosResult)
        first_order_indices = ot.Point(
            [chaosSI.getSobolIndex(i) for i in range(dimension)]
        )
        total_order_indices = ot.Point(
            [chaosSI.getSobolTotalIndex(i) for i in range(dimension)]
        )
        result = SparsePolynomialChaosSensitivityResult(
            predictivity_coefficient, first_order_indices, total_order_indices
        )
        return result
