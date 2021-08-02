# -*- coding: utf-8 -*-
"""
Test for SensitivityConvergence class.
"""
import otbenchmark as otb
import unittest
import openturns.viewer as otv
import openturns as ot
import numpy as np


class CheckSensitivityConvergence(unittest.TestCase):
    def test_plotConvergenceGrid(self):
        ot.Log.Show(ot.Log.NONE)
        problem = otb.IshigamiSensitivity()
        metaSAAlgorithm = otb.SensitivityBenchmarkMetaAlgorithm(problem)
        benchmark = otb.SensitivityConvergence(
            problem,
            metaSAAlgorithm,
            numberOfExperiments=12,
            numberOfRepetitions=4,
            maximum_elapsed_time=1.0,
            sample_size_initial=20,
            estimator="Saltelli",
            sampling_method="MonteCarlo",
        )
        grid = benchmark.plotConvergenceGrid(verbose=True)
        otv.View(grid)

    def test_computeError(self):
        ot.Log.Show(ot.Log.NONE)
        problem = otb.IshigamiSensitivity()
        metaSAAlgorithm = otb.SensitivityBenchmarkMetaAlgorithm(problem)
        benchmark = otb.SensitivityConvergence(
            problem,
            metaSAAlgorithm,
            numberOfExperiments=12,
            numberOfRepetitions=4,
            maximum_elapsed_time=1.0,
            sample_size_initial=20,
        )
        sample_size = 40000
        first_order_AE, total_order_AE = benchmark.computeError(sample_size)
        print(sample_size, first_order_AE, total_order_AE)
        atol = 1.0e1 / np.sqrt(sample_size)
        zeros = ot.Point(3)
        np.testing.assert_allclose(zeros, first_order_AE, atol=atol)
        np.testing.assert_allclose(zeros, total_order_AE, atol=atol)
        print(first_order_AE)
        print(total_order_AE)

    def test_computeSobolSample(self):
        ot.Log.Show(ot.Log.NONE)
        problem = otb.IshigamiSensitivity()
        metaSAAlgorithm = otb.SensitivityBenchmarkMetaAlgorithm(problem)
        benchmark = otb.SensitivityConvergence(
            problem,
            metaSAAlgorithm,
            numberOfExperiments=12,
            numberOfRepetitions=4,
            maximum_elapsed_time=5.0,
            sample_size_initial=20,
        )
        (
            sample_size_table,
            first_order_table,
            total_order_table,
        ) = benchmark.computeSobolSample()
        print(total_order_table)

    def test_plotConvergenceCurve(self):
        ot.Log.Show(ot.Log.NONE)
        problem = otb.IshigamiSensitivity()
        metaSAAlgorithm = otb.SensitivityBenchmarkMetaAlgorithm(problem)
        benchmark = otb.SensitivityConvergence(
            problem,
            metaSAAlgorithm,
            numberOfExperiments=12,
            numberOfRepetitions=4,
            maximum_elapsed_time=1.0,
            sample_size_initial=20,
            estimator="Saltelli",
            sampling_method="MonteCarlo",
        )
        grid = benchmark.plotConvergenceCurve(verbose=True)
        otv.View(grid)


if __name__ == "__main__":
    unittest.main()
