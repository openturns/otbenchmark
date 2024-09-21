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
        exact_first_order = problem.getFirstOrderIndices()
        exact_total_order = problem.getTotalOrderIndices()
        metaSAAlgorithm = otb.SensitivityBenchmarkMetaAlgorithm(problem)
        sample_size = 100000
        # By Monte-Carlo
        for sampling_method in ["MonteCarlo", "LHS", "QMC"]:
            print("sampling_method=", sampling_method)
            (
                computed_first_order,
                computed_total_order,
            ) = metaSAAlgorithm.runSamplingEstimator(
                sample_size, sampling_method=sampling_method
            )
            print(exact_first_order - computed_first_order)
            print(exact_total_order - computed_total_order)
            if sampling_method == "QMC":
                atol = 1.0e2 / sample_size
            else:
                atol = 1.0e1 / np.sqrt(sample_size)
            np.testing.assert_allclose(
                exact_first_order, computed_first_order, atol=atol
            )
            np.testing.assert_allclose(
                exact_total_order, computed_total_order, atol=atol
            )
        # By Martinez
        for estimator in [
            "Saltelli",
            "Jansen",
            "MauntzKucherenko",
            "Martinez",
            "Janon",
        ]:
            print("estimator=", estimator)
            (
                computed_first_order,
                computed_total_order,
            ) = metaSAAlgorithm.runSamplingEstimator(sample_size, estimator=estimator)
            atol = 1.0e1 / np.sqrt(sample_size)
            np.testing.assert_allclose(
                exact_first_order, computed_first_order, atol=atol
            )
            np.testing.assert_allclose(
                exact_total_order, computed_total_order, atol=atol
            )
            print(exact_first_order - computed_first_order)
            print(exact_total_order - computed_total_order)


if __name__ == "__main__":
    unittest.main()
