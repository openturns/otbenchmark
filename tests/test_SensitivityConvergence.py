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
            maximumElapsedTime=1.0,
            sampleSizeInitial=20,
            estimator="Saltelli",
            samplingMethod="MonteCarlo",
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
            maximumElapsedTime=1.0,
            sampleSizeInitial=20,
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
            maximumElapsedTime=5.0,
            sampleSizeInitial=20,
        )
        (
            _,
            _,
            totalOrderTable,
        ) = benchmark.computeSobolSample()
        print(totalOrderTable)

    def test_plotConvergenceCurveSampling(self):
        ot.Log.Show(ot.Log.NONE)
        problem = otb.IshigamiSensitivity()
        metaSAAlgorithm = otb.SensitivityBenchmarkMetaAlgorithm(problem)
        benchmark = otb.SensitivityConvergence(
            problem,
            metaSAAlgorithm,
            numberOfExperiments=12,
            numberOfRepetitions=4,
            maximumElapsedTime=1.0,
            sampleSizeInitial=20,
            estimator="Saltelli",
            samplingMethod="MonteCarlo",
        )
        graph = benchmark.plotConvergenceCurve(verbose=True)
        otv.View(graph)

    def test_plotConvergenceCurveChaos(self):
        ot.Log.Show(ot.Log.NONE)
        problem = otb.IshigamiSensitivity()
        metaSAAlgorithm = otb.SensitivityBenchmarkMetaAlgorithm(problem)
        benchmark = otb.SensitivityConvergence(
            problem,
            metaSAAlgorithm,
            numberOfExperiments=12,
            numberOfRepetitions=1,
            maximumElapsedTime=2.0,
            sampleSizeInitial=80,
            useSampling=False,
            totalDegree=5,
            hyperbolicQuasiNorm=1.0,
        )
        graph = benchmark.plotConvergenceCurve(verbose=True)
        graph.setLegendPosition("bottomleft")
        otv.View(graph)


if __name__ == "__main__":
    unittest.main()
