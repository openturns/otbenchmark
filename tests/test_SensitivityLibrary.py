"""
Test for SensitivityLibrary class.
"""
import otbenchmark as otb
import unittest


class CheckSensitivityLibrary(unittest.TestCase):
    def test_SensitivityBenchmarkProblemList(self):
        benchmarkProblemList = otb.SensitivityBenchmarkProblemList()
        numberOfProblems = len(benchmarkProblemList)
        for i in range(numberOfProblems):
            problem = benchmarkProblemList[i]
            name = problem.getName()
            first_order_indices = problem.getFirstOrderIndices()
            total_order_indices = problem.getTotalOrderIndices()
            dimension = problem.getInputDistribution().getDimension()
            print(
                "#",
                i,
                ":",
                name,
                " : S = ",
                first_order_indices,
                "T=",
                total_order_indices,
                ", dimension=",
                dimension,
            )


if __name__ == "__main__":
    unittest.main()
