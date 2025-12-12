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
        self, sampleSize, estimator="Saltelli", samplingMethod="MonteCarlo"
    ):
        """
        Runs the sampling sensitivity estimator and get the results.

        We may let the user select the estimator by taking
        e.g. the :class:`ot.SaltelliSensitivityAlgorithm` as input argument,
        and use :meth:`ot.SaltelliSensitivityAlgorithm.setDesign`, but this currently fails:
        https://github.com/openturns/openturns/issues/1884
        This is why the estimator input argument is currently a string.

        Parameters
        ----------
        sampleSize: int
            The sample size.
        estimator : str
            The estimator.
            Must be "Saltelli", "Jansen", "Martinez", "MauntzKucherenko".
        samplingMethod : str
            The sampling method.
            Must be "MonteCarlo" or "LHS" or "QMC".

        Returns
        -------
        firstOrder: ot.Point(dimension)
            The Sobol' first order indices.
        totalOrder: ot.Point(dimension)
            The Sobol' total order indices.
        """
        if (
            samplingMethod == "MonteCarlo"
            or samplingMethod == "LHS"
            or samplingMethod == "QMC"
        ):
            ot.ResourceMap.SetAsString(
                "SobolIndicesExperiment-SamplingMethod", samplingMethod
            )
        else:
            raise ValueError(
                f"Unknown value of sampling method : {samplingMethod}"
            )
        distribution = self.problem.getInputDistribution()
        model = self.problem.getFunction()
        experiment = ot.SobolIndicesExperiment(distribution, sampleSize)
        inputDesign = experiment.generate()
        outputDesign = model(inputDesign)
        if estimator == "Janon":
            sobolAlgorithm = otb.JanonSensitivityAlgorithm(
                inputDesign, outputDesign, sampleSize
            )
        else:
            if estimator == "Saltelli":
                sobolAlgorithm = ot.SaltelliSensitivityAlgorithm()
            elif estimator == "Jansen":
                sobolAlgorithm = ot.JansenSensitivityAlgorithm()
            elif estimator == "Martinez":
                sobolAlgorithm = ot.MartinezSensitivityAlgorithm()
            elif estimator == "MauntzKucherenko":
                sobolAlgorithm = ot.MauntzKucherenkoSensitivityAlgorithm()
            else:
                raise ValueError(f"Unknown value of estimator {estimator}")
            sobolAlgorithm.setDesign(inputDesign, outputDesign, sampleSize)
        firstOrder = sobolAlgorithm.getFirstOrderIndices()
        totalOrder = sobolAlgorithm.getTotalOrderIndices()
        return firstOrder, totalOrder

    def runPolynomialChaosEstimator(
        self,
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
        sampleSizeTrain : int, optional
            The training sample size. The default is 100.
        sampleSizeTest : int, optional
            The test sample size. The default is 100.
        totalDegree : int, optional
            The total polynomial degree. The default is 2.
        hyperbolicQuasiNorm : float, optional
            The hyperbolic quasi-norm. The default is 0.5.
        sparse : bool, optional
            Whether to use sparse polynomial chaos. The default is True.

        Returns
        -------
        firstOrder: ot.Point(dimension)
            The Sobol' first order indices.
        totalOrder: ot.Point(dimension)
            The Sobol' total order indices.
        """
        sparse_sa = otb.SparsePolynomialChaosSensitivityAnalysis(
            self.problem,
            sampleSizeTrain=sampleSizeTrain,
            sampleSizeTest=sampleSizeTest,
            totalDegree=totalDegree,
            hyperbolicQuasiNorm=hyperbolicQuasiNorm,
            sparse=sparse,
        )
        result = sparse_sa.run()
        return result.firstOrderIndices, result.totalOrderIndices
