# -*- coding: utf-8 -*-
# Copyright 2020 EDF.
"""
Test for IshigamiSensitivityBenchmarkProblem class.
"""
import openturns as ot
import otbenchmark as otb
import unittest
import numpy as np


class CheckDrawEvent(unittest.TestCase):
    def test_DrawLimitState(self):
        problem = otb.IshigamiSensitivityBenchmarkProblem()
        distribution = problem.getInputDistribution()
        model = problem.getFunction()

        # Create X/Y data
        ot.RandomGenerator.SetSeed(0)
        size = 10000
        inputDesign = ot.SobolIndicesExperiment(distribution, size, True).generate()
        outputDesign = model(inputDesign)

        # Compute first order indices using the Saltelli estimator
        sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(
            inputDesign, outputDesign, size
        )
        computed_first_order = sensitivityAnalysis.getFirstOrderIndices()
        computed_total_order = sensitivityAnalysis.getTotalOrderIndices()

        # Exact first and total order
        exact_first_order = problem.getFirstOrderIndices()
        exact_total_order = problem.getTotalOrderIndices()

        # Compare with exact results
        print("Sample size : ", size)
        atol = 10.0 / np.sqrt(size)
        print("Absolute Tolerance = ", atol)
        # First order
        # Compute absolute error (the LRE cannot be computed,
        # because S can be zero)
        print("Computed first order = ", computed_first_order)
        print("Exact first order = ", exact_first_order)
        np.testing.assert_allclose(computed_first_order, exact_first_order, atol=atol)
        # Total order
        print("Computed total order = ", computed_total_order)
        print("Exact total order = ", exact_total_order)
        np.testing.assert_allclose(computed_total_order, exact_total_order, atol=atol)


if __name__ == "__main__":
    unittest.main()
