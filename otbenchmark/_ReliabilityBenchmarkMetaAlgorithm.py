# -*- coding: utf-8 -*-
"""
Manage reliability problems.
"""
import otbenchmark as otb


class ReliabilityBenchmarkMetaAlgorithm:
    def __init__(self, problem):
        """
        Create a meta-algorithm to solve a reliability problem.


        Parameters
        ----------
        problem : ot.ReliabilityBenchmarkProblem
            The problem.
        """
        #
        self.problem = problem
        return None

    def runFORM(self, nearestPointAlgorithm):
        """
        Runs the FORM algorithm and get the results.

        Parameters
        ----------
        nearestPointAlgorithm : ot.OptimizationAlgorithm
            Optimization algorithm used to search the design point.

        Returns
        -------
        result : ReliabilityBenchmarkResult
            The problem result.
        """
        algo = otb.FORM(self.problem, nearestPointAlgorithm)
        event = self.problem.getEvent()
        g = event.getFunction()
        initialNumberOfCall = g.getEvaluationCallsNumber()
        try:
            algo.run()
            resultFORM = algo.getResult()
            computedProbability = resultFORM.getEventProbability()
        except RuntimeError:
            computedProbability = 0.0
        numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
        pfReference = self.problem.getProbability()
        result = otb.ReliabilityBenchmarkResult(
            pfReference, computedProbability, numberOfFunctionEvaluations
        )
        return result

    def runSORM(self, nearestPointAlgorithm):
        """
        Runs the SORM algorithm and get the results.

        Parameters
        ----------
        nearestPointAlgorithm : ot.OptimizationAlgorithm
            Optimization algorithm used to search the design point.

        Returns
        -------
        result : ReliabilityBenchmarkResult
            The problem result.
        """
        event = self.problem.getEvent()
        g = event.getFunction()
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algo = otb.SORM(self.problem, nearestPointAlgorithm)
        try:
            algo.run()
            resultSORM = algo.getResult()
            computedProbability = resultSORM.getEventProbabilityBreitung()
        except RuntimeError:
            computedProbability = 0.0
        numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
        pfReference = self.problem.getProbability()
        result = otb.ReliabilityBenchmarkResult(
            pfReference, computedProbability, numberOfFunctionEvaluations
        )
        return result

    def runMonteCarlo(
        self, maximumOuterSampling=1000, coefficientOfVariation=0.1, blockSize=1
    ):
        """
        Runs the ProbabilitySimulationAlgorithm with Monte-Carlo experiment
        algorithm and get results.

        Parameters
        ----------
        maximumOuterSampling : int
            The maximum number of outer iterations.
        coefficientOfVariation : float
            The maximum coefficient of variation.
        blockSize : int
            The number of inner iterations.

        Returns
        -------
        result : ReliabilityBenchmarkResult
            The problem result.
        """
        event = self.problem.getEvent()
        g = event.getFunction()
        factory = otb.ProbabilitySimulationAlgorithmFactory()
        algo = factory.buildMonteCarlo(self.problem)
        algo.setMaximumOuterSampling(maximumOuterSampling)
        algo.setBlockSize(blockSize)
        algo.setMaximumCoefficientOfVariation(coefficientOfVariation)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algo.run()
        resultMC = algo.getResult()
        numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
        computedProbability = resultMC.getProbabilityEstimate()
        pfReference = self.problem.getProbability()
        result = otb.ReliabilityBenchmarkResult(
            pfReference, computedProbability, numberOfFunctionEvaluations
        )
        return result

    def runFORMImportanceSampling(
        self,
        nearestPointAlgorithm,
        maximumOuterSampling=1000,
        coefficientOfVariation=0.1,
        blockSize=1,
    ):
        """
        Runs the Importance Sampling method with FORM importance
        distribution and get the number of function evaluations.

        Parameters
        ----------
        nearestPointAlgorithm : ot.OptimizationAlgorithm
            Optimization algorithm used to search the design point.
        maximumOuterSampling : int
            The maximum number of outer iterations.
        coefficientOfVariation : float
            The maximum coefficient of variation.
        blockSize : int
            The number of inner iterations.

        Returns
        -------
        result : ReliabilityBenchmarkResult
            The problem result.
        """
        factory = otb.ProbabilitySimulationAlgorithmFactory()
        event = self.problem.getEvent()
        g = event.getFunction()
        initialNumberOfCall = g.getEvaluationCallsNumber()
        try:
            algo = factory.buildFORMIS(self.problem, nearestPointAlgorithm)
            algo.setMaximumCoefficientOfVariation(coefficientOfVariation)
            algo.setMaximumOuterSampling(maximumOuterSampling)
            algo.setBlockSize(blockSize)
            algo.run()
            result = algo.getResult()
            computedProbability = result.getProbabilityEstimate()
        except RuntimeError:
            computedProbability = 0.0
        numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
        pfReference = self.problem.getProbability()
        result = otb.ReliabilityBenchmarkResult(
            pfReference, computedProbability, numberOfFunctionEvaluations
        )
        return result

    def runSubsetSampling(
        self, maximumOuterSampling=1000, coefficientOfVariation=0.1, blockSize=1
    ):
        """
        Runs the Subset method and get the results.

        Parameters
        ----------
        maximumOuterSampling : int
            The maximum number of outer iterations.
        coefficientOfVariation : float
            The maximum coefficient of variation.
        blockSize : int
            The number of inner iterations.

        Returns
        -------
        result : ReliabilityBenchmarkResult
            The problem result.
        """
        event = self.problem.getEvent()
        g = event.getFunction()
        algo = otb.SubsetSampling(self.problem)
        algo.setMaximumOuterSampling(maximumOuterSampling)
        algo.setMaximumCoefficientOfVariation(coefficientOfVariation)
        algo.setBlockSize(blockSize)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algo.run()
        resultSS = algo.getResult()
        computedProbability = resultSS.getProbabilityEstimate()
        pfReference = self.problem.getProbability()
        numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
        result = otb.ReliabilityBenchmarkResult(
            pfReference, computedProbability, numberOfFunctionEvaluations
        )
        return result

    def runLHS(
        self, maximumOuterSampling=1000, coefficientOfVariation=0.1, blockSize=1
    ):
        """
        Runs the LHS algorithm and get the results.

        Parameters
        ----------
        maximumOuterSampling : int
            The maximum number of outer iterations.
        coefficientOfVariation : float
            The maximum coefficient of variation.
        blockSize : int
            The number of inner iterations.

        Returns
        -------
        result : ReliabilityBenchmarkResult
            The problem result.
        """
        event = self.problem.getEvent()
        g = event.getFunction()
        algo = otb.LHS(self.problem)
        initialNumberOfCall = g.getEvaluationCallsNumber()
        algo.setMaximumCoefficientOfVariation(coefficientOfVariation)
        algo.setMaximumOuterSampling(maximumOuterSampling)
        algo.run()
        numberOfFunctionEvaluations = g.getEvaluationCallsNumber() - initialNumberOfCall
        result = algo.getResult()
        computedProbability = result.getProbabilityEstimate()
        pfReference = self.problem.getProbability()
        result = otb.ReliabilityBenchmarkResult(
            pfReference, computedProbability, numberOfFunctionEvaluations
        )
        return result
