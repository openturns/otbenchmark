"""
Estimate sensitivity indices from sparse polynomial chaos
with hyperbolic enumerate function and regression.
"""

import openturns as ot


class SparsePolynomialChaosSensitivityResult:
    def __init__(
        self, predictivityCoefficient, firstOrderIndices, totalOrderIndices
    ):
        """
        The result of the sensitivity analysis from polynomial chaos.

        Parameters
        ----------
        predictivityCoefficient : float
            The predictivity coefficient. Always lower or equal to 1.
            Close to 1 is better.
            Lower than 0.5 means that the polynomial chaos metamodel
            cannot be trusted.
        firstOrderIndices : ot.Point(d)
            The first order sensitivity indices.
        totalOrderIndices : ot.Point(d)
            The total order sensitivity indices.

        Returns
        -------
        None.

        """
        self.predictivityCoefficient = predictivityCoefficient
        self.firstOrderIndices = firstOrderIndices
        self.totalOrderIndices = totalOrderIndices


class SparsePolynomialChaosSensitivityAnalysis:
    def __init__(
        self,
        sensitivityBenchmarkProblem,
        sampleSizeTrain=100,
        sampleSizeTest=100,
        totalDegree=2,
        hyperbolicQuasiNorm=0.5,
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
        sampleSizeTrain : int, optional
            The training sample size. The default is 100.
        sampleSizeTest : int, optional
            The test sample size. The default is 100.
        totalDegree : int, optional
            The total polynomial degree. The default is 2.
        hyperbolicQuasiNorm : float, optional
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
        self.sampleSizeTrain = sampleSizeTrain
        self.sampleSizeTest = sampleSizeTest
        self.totalDegree = totalDegree
        self.hyperbolicQuasiNorm = hyperbolicQuasiNorm
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
            print(f"Generate train experiment, N={self.sampleSizeTrain}")
        sequence = ot.SobolSequence(dimension)
        experiment = ot.LowDiscrepancyExperiment(
            sequence, distribution, self.sampleSizeTrain
        )
        inputTrain = experiment.generate()
        outputTrain = model(inputTrain)

        # Create polynomial chaos expansion
        if verbose:
            print("Create polynomial chaos expansion..")
        distributionList = [distribution.getMarginal(i) for i in range(dimension)]
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
            dimension, self.hyperbolicQuasiNorm
        )
        multivariateBasis = ot.OrthogonalProductPolynomialFactory(
            polyColl, enumerateFunction
        )
        basisDimension = enumerateFunction.getBasisSizeFromTotalDegree(self.totalDegree)
        if verbose:
            print(f"> Sparse = {self.sparse}")
            print(f"> Total degree = {self.totalDegree}")
            print(f"> Basis dimension = {basisDimension}")
        if basisDimension >= self.sampleSizeTrain:
            raise ValueError(
                f"The number of candidate coefficients is {basisDimension} "
                f"is larger or equal to the sample size {self.sampleSizeTrain}"
            )
        adaptiveStrategy = ot.FixedStrategy(multivariateBasis, basisDimension)
        chaosAlgorithm = ot.FunctionalChaosAlgorithm(
            inputTrain, outputTrain, distribution, adaptiveStrategy, projectionStrategy
        )
        if verbose:
            print("> Fit")
        chaosAlgorithm.run()
        chaosResult = chaosAlgorithm.getResult()
        number_of_coefficients = chaosResult.getCoefficients().getSize()
        if verbose:
            print(f"> Number of selected coefficients: {number_of_coefficients}")

        # Validation
        if verbose:
            print("> Validation...")
            print(f"> Generate test experiment, N={self.sampleSizeTest}")
        metamodel = chaosResult.getMetaModel()  # get the metamodel
        experiment = ot.MonteCarloExperiment(distribution, self.sampleSizeTest)
        inputTest = experiment.generate()
        outputTest = model(inputTest)
        predictions = metamodel(inputTest)
        val = ot.MetaModelValidation(outputTest, predictions)
        predictivityCoefficient = val.computeR2Score()[0]
        if verbose:
            print(f"> Q2={100 * predictivityCoefficient:0.2f}%")

        # S.A.
        if verbose:
            print("> Sensitivity Analysis...")
        chaosSI = ot.FunctionalChaosSobolIndices(chaosResult)
        firstOrderIndices = ot.Point(
            [chaosSI.getSobolIndex(i) for i in range(dimension)]
        )
        totalOrderIndices = ot.Point(
            [chaosSI.getSobolTotalIndex(i) for i in range(dimension)]
        )
        result = SparsePolynomialChaosSensitivityResult(
            predictivityCoefficient, firstOrderIndices, totalOrderIndices
        )
        return result
