"""
Test for ReliabilityLibrary class.
"""
import otbenchmark as otb
import unittest
import numpy as np


class CheckReliabilityLibrary(unittest.TestCase):
    def test_ComputeLogRelativeError(self):
        lre = otb.ComputeLogRelativeError(1.234, 1.235)
        np.testing.assert_almost_equal(lre, 3.0913151)
        lre = otb.ComputeLogRelativeError(1.234, 0.0)
        np.testing.assert_almost_equal(lre, 0.0)
        lre = otb.ComputeLogRelativeError(0.0, 1.234)
        np.testing.assert_almost_equal(lre, 0.0)
        lre = otb.ComputeLogRelativeError(0.5, 0.5)
        np.testing.assert_almost_equal(lre, 15.65355977452702)
        lre = otb.ComputeLogRelativeError(0.5, np.inf)
        np.testing.assert_almost_equal(lre, 0.0)
        lre = otb.ComputeLogRelativeError(np.inf, 0.5)
        np.testing.assert_almost_equal(lre, 0.0)

    def test_ComputeAbsoluteError(self):
        ae = otb.ComputeAbsoluteError(1.0, 1.1)
        np.testing.assert_almost_equal(ae, 0.1)

    def test_ComputeRelativeError(self):
        re = otb.ComputeRelativeError(1.0, 1.1)
        np.testing.assert_almost_equal(re, 0.1)

    def test_ReliabilityBenchmarkProblemList(self):
        benchmarkProblemList = otb.ReliabilityBenchmarkProblemList()
        numberOfProblems = len(benchmarkProblemList)
        for i in range(numberOfProblems):
            problem = benchmarkProblemList[i]
            name = problem.getName()
            pf = problem.getProbability()
            event = problem.getEvent()
            antecedent = event.getAntecedent()
            distribution = antecedent.getDistribution()
            dimension = distribution.getDimension()
            print("#", i, ":", name, " : pf = ", pf, ", dimension=", dimension)


if __name__ == "__main__":
    unittest.main()
