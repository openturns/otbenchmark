# Copyright 2020 EDF.
"""
Test for GaussianProductSensitivity class.
"""
import openturns as ot
import otbenchmark as otb
import unittest
import numpy as np


class CheckGaussianProduct(unittest.TestCase):
    def test_GaussianProduct(self):
        problem = otb.GaussianProductSensitivity()
        print(problem)
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
        atol = 5.0 / np.sqrt(size)
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

    def test_GaussianProduct2(self):
        mu = [1.5, 3.5]
        sigma = [0.5, 2.5]
        problem = otb.GaussianProductSensitivity(mu, sigma)
        print(problem)
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

        # Check exact results
        Sexact = [0.1638796, 0.7525084]
        Texact = [0.2474916, 0.8361204]
        np.testing.assert_allclose(Sexact, exact_first_order, rtol=1.0e-6)
        np.testing.assert_allclose(Texact, exact_total_order, rtol=1.0e-6)

        # Compare with exact results
        print("Sample size : ", size)
        atol = 5.0 / np.sqrt(size)
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


def test_GaussianProduct3(self):
    mu = [0.1, 0.0]
    sigma = [0.5, 2.5]
    problem = otb.GaussianProductSensitivity(mu, sigma)
    print(problem)
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

    # Check exact results
    Sexact = [0.0, 0.0384615]
    Texact = [0.9615385, 1.0]
    np.testing.assert_allclose(Sexact, exact_first_order, rtol=1.0e-6)
    np.testing.assert_allclose(Texact, exact_total_order, rtol=1.0e-6)

    # Compare with exact results
    print("Sample size : ", size)
    atol = 5.0 / np.sqrt(size)
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
