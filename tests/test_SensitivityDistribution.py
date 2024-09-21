"""
Test for SensitivityDistribution class.
"""
import otbenchmark as otb
import unittest
import openturns.viewer as otv
import openturns as ot


class CheckSensitivityDistribution(unittest.TestCase):
    def test_draw(self):
        ot.Log.Show(ot.Log.NONE)
        problem = otb.IshigamiSensitivity()
        metaSAAlgorithm = otb.SensitivityBenchmarkMetaAlgorithm(problem)
        benchmark = otb.SensitivityDistribution(
            problem, metaSAAlgorithm, sampleSize=500, numberOfRepetitions=50,
        )
        grid = benchmark.draw()
        otv.View(grid)


if __name__ == "__main__":
    unittest.main()
