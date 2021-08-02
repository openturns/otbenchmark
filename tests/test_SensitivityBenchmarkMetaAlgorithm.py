# -*- coding: utf-8 -*-
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
        (
            computed_first_order,
            computed_total_order,
        ) = metaSAAlgorithm.runSamplingEstimator(sample_size)
        atol = 1.0e1 / np.sqrt(sample_size)
        np.testing.assert_allclose(exact_first_order, computed_first_order, atol=atol)
        np.testing.assert_allclose(exact_total_order, computed_total_order, atol=atol)
        print(exact_first_order - computed_first_order)
        print(exact_total_order - computed_total_order)
        # By Quasi-Monte-Carlo
        (
            computed_first_order,
            computed_total_order,
        ) = metaSAAlgorithm.runSamplingEstimator(sample_size, sampling_method="QMC")
        atol = 1.0e3 / sample_size
        np.testing.assert_allclose(exact_first_order, computed_first_order, atol=atol)
        np.testing.assert_allclose(exact_total_order, computed_total_order, atol=atol)
        print(exact_first_order - computed_first_order)
        print(exact_total_order - computed_total_order)
        # By Martinez
        (
            computed_first_order,
            computed_total_order,
        ) = metaSAAlgorithm.runSamplingEstimator(sample_size, estimator="Martinez")
        atol = 1.0e1 / np.sqrt(sample_size)
        np.testing.assert_allclose(exact_first_order, computed_first_order, atol=atol)
        np.testing.assert_allclose(exact_total_order, computed_total_order, atol=atol)
        print(exact_first_order - computed_first_order)
        print(exact_total_order - computed_total_order)


if __name__ == "__main__":
    unittest.main()
