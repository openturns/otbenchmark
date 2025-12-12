"""
Test for SensitivityBenchmarkMetaAlgorithm class.
"""
import otbenchmark as otb
import unittest
import openturns as ot
import numpy as np


class CheckSensitivityBenchmarkMetaAlgorithm(unittest.TestCase):
    def test_SensitivityBenchmarkMetaAlgorithm(self):
        ot.Log.Show(ot.Log.NONE)
        problem = otb.IshigamiSensitivity()
        exactFirstOrder = problem.getFirstOrderIndices()
        exactTotalOrder = problem.getTotalOrderIndices()
        metaSAAlgorithm = otb.SensitivityBenchmarkMetaAlgorithm(problem)
        sampleSize = 100000
        # By Monte-Carlo
        for samplingMethod in ["MonteCarlo", "LHS", "QMC"]:
            print("samplingMethod=", samplingMethod)
            (
                computedFirstOrder,
                computedTotalOrder,
            ) = metaSAAlgorithm.runSamplingEstimator(
                sampleSize, samplingMethod=samplingMethod
            )
            print(exactFirstOrder - computedFirstOrder)
            print(exactTotalOrder - computedTotalOrder)
            if samplingMethod == "QMC":
                atol = 1.0e2 / sampleSize
            else:
                atol = 1.0e1 / np.sqrt(sampleSize)
            np.testing.assert_allclose(
                exactFirstOrder, computedFirstOrder, atol=atol
            )
            np.testing.assert_allclose(
                exactTotalOrder, computedTotalOrder, atol=atol
            )
        for estimator in [
            "Saltelli",
            "Jansen",
            "MauntzKucherenko",
            "Martinez",
            "Janon",
        ]:
            print("estimator=", estimator)
            (
                computedFirstOrder,
                computedTotalOrder,
            ) = metaSAAlgorithm.runSamplingEstimator(sampleSize, estimator=estimator)
            atol = 1.0e1 / np.sqrt(sampleSize)
            np.testing.assert_allclose(
                exactFirstOrder, computedFirstOrder, atol=atol
            )
            np.testing.assert_allclose(
                exactTotalOrder, computedTotalOrder, atol=atol
            )
            print(exactFirstOrder - computedFirstOrder)
            print(exactTotalOrder - computedTotalOrder)


if __name__ == "__main__":
    unittest.main()
