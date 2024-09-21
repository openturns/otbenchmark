# -*- coding: utf-8 -*-
"""
Manage reliability problems.
"""
import otbenchmark as otb


class ReliabilityBenchmarkResult:
    def __init__(
        self, exactProbability, computedProbability, numberOfFunctionEvaluations
    ):
        """
        Create a benchmark result for a reliability problem.

        Parameters
        ----------
        exactProbability: float
            The exact probability.
        computedProbability: float
            The estimated probability.
        numberOfFunctionEvaluations: int
            The number of function evaluations.

        Attributes
        ----------
        absoluteError: float
            The absolute error of the estimated probability.
        numberOfCorrectDigits: float
            The log-relative error in base 10.
        numberOfDigitsPerEvaluation: float
            The number of correct digits per function evaluation.
        """
        self.computedProbability = computedProbability
        self.exactProbability = exactProbability
        absoluteError = abs(computedProbability - exactProbability)
        self.absoluteError = absoluteError
        numberOfCorrectDigits = otb.ComputeLogRelativeError(
            exactProbability, computedProbability
        )
        self.numberOfCorrectDigits = numberOfCorrectDigits
        self.numberOfFunctionEvaluations = numberOfFunctionEvaluations
        self.numberOfDigitsPerEvaluation = (
            self.numberOfCorrectDigits / self.numberOfFunctionEvaluations
        )
        return None

    def summary(self):
        """
        Returns a string which presents a summary of the reliability benchmark.
        """
        s = (
            "computedProbability = %s\n"
            "exactProbability = %s\n"
            "absoluteError = %s\n"
            "numberOfCorrectDigits = %s\n"
            "numberOfFunctionEvaluations = %s\n"
            "numberOfDigitsPerEvaluation = %s"
        ) % (
            self.computedProbability,
            self.exactProbability,
            self.absoluteError,
            self.numberOfCorrectDigits,
            self.numberOfFunctionEvaluations,
            self.numberOfDigitsPerEvaluation,
        )
        return s
