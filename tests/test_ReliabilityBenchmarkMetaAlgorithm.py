"""
Test for ReliabilityBenchmarkMetaAlgorithm class.
"""
import otbenchmark as otb
import unittest
import openturns as ot


class CheckReliabilityBenchmarkMetaAlgorithm(unittest.TestCase):
    def test_ReliabilityBenchmarkMetaAlgorithm(self):
        maximumEvaluationNumber = 1000
        maximumAbsoluteError = 1.0e-3
        maximumRelativeError = 1.0e-3
        maximumResidualError = 1.0e-3
        maximumConstraintError = 1.0e-3
        nearestPointAlgorithm = ot.AbdoRackwitz()
        nearestPointAlgorithm.setMaximumCallsNumber(maximumEvaluationNumber)
        nearestPointAlgorithm.setMaximumAbsoluteError(maximumAbsoluteError)
        nearestPointAlgorithm.setMaximumRelativeError(maximumRelativeError)
        nearestPointAlgorithm.setMaximumResidualError(maximumResidualError)
        nearestPointAlgorithm.setMaximumConstraintError(maximumConstraintError)
        problem = otb.ReliabilityProblem8()
        metaAlgorithm = otb.ReliabilityBenchmarkMetaAlgorithm(problem)
        benchmarkResult = metaAlgorithm.runFORM(nearestPointAlgorithm)
        print(benchmarkResult.summary())
        benchmarkResult = metaAlgorithm.runSORM(nearestPointAlgorithm)
        print(benchmarkResult.summary())
        benchmarkResult = metaAlgorithm.runLHS(maximumOuterSampling=10000)
        print(benchmarkResult.summary())
        benchmarkResult = metaAlgorithm.runMonteCarlo(maximumOuterSampling=10000)
        print(benchmarkResult.summary())
        benchmarkResult = metaAlgorithm.runFORMImportanceSampling(nearestPointAlgorithm)
        print(benchmarkResult.summary())
        benchmarkResult = metaAlgorithm.runSubsetSampling()
        print(benchmarkResult.summary())


if __name__ == "__main__":
    unittest.main()
