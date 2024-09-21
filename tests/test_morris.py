# Copyright 2021 EDF.
"""
Test for MorrisSensitivity class.
"""
import otbenchmark as otb
import unittest


class CheckMorrisSensitivity(unittest.TestCase):
    def test_Morris(self):
        problem = otb.MorrisSensitivity()
        print(problem)
        distribution = problem.getInputDistribution()
        model = problem.getFunction()
        exact_first_order = problem.getFirstOrderIndices()
        exact_total_order = problem.getTotalOrderIndices()

        assert distribution.getDimension() == 20
        assert model.getInputDimension() == 20
        assert model.getOutputDimension() == 1
        assert exact_first_order.getDimension() == 20
        assert exact_total_order.getDimension() == 20

        # Check we can call it
        input_sample = distribution.getSample(10)
        output_sample = model(input_sample)
        assert output_sample.getSize() == 10

    def test_MorrisRandom(self):
        problem = otb.MorrisSensitivity(random_parameters=True)
        print(problem)
        distribution = problem.getInputDistribution()
        model = problem.getFunction()
        exact_first_order = problem.getFirstOrderIndices()
        exact_total_order = problem.getTotalOrderIndices()

        assert distribution.getDimension() == 20
        assert model.getInputDimension() == 20
        assert model.getOutputDimension() == 1
        assert exact_first_order.getDimension() == 20
        assert exact_total_order.getDimension() == 20

        # Check we can call it
        input_sample = distribution.getSample(10)
        output_sample = model(input_sample)
        assert output_sample.getSize() == 10


if __name__ == "__main__":
    unittest.main()
