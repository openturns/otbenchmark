# Copyright 2020 EDF.
"""
Test for ConditionalDistribution class.
"""
import openturns as ot
import otbenchmark
import unittest
import numpy as np
import openturns.viewer as otv


class CheckConditionalDistribution(unittest.TestCase):
    def test_ComputeExtendedInput(self):
        # The random variable is (X0, X1, X2)
        distribution = ot.Normal(3)
        # We condition with respect to X1=mu1, i.e.
        # we consider (X0, X1, X2) | X1=2
        X = [1.1, 3.3]
        conditionalIndices = [1]
        conditionalReferencePoint = [2.2]
        conditionalDistribution = otbenchmark.ConditionalDistribution(
            distribution, conditionalIndices, conditionalReferencePoint
        )
        extendedX = conditionalDistribution.computeExtendedInput(X)
        np.testing.assert_equal(extendedX, ot.Point([1.1, 2.2, 3.3]))

    def test_ConditionalDistribution1(self):
        # The random variable is (X0, X1, X2)
        distribution = ot.Normal(3)
        # We condition with respect to X1=mu1, i.e.
        # we consider (X0, X1, X2) | X1=2
        conditionalIndices = [1]
        conditionalReferencePoint = [2.0]
        conditionalDistribution = ot.Distribution(
            otbenchmark.ConditionalDistribution(
                distribution, conditionalIndices, conditionalReferencePoint
            )
        )
        # PDF
        computed = conditionalDistribution.computePDF([1.0, 1.0])
        print("computed PDF=", computed)
        conditionedPDF = distribution.computePDF(
            [1.0, 1.0, conditionalReferencePoint[0]]
        )
        n1 = ot.Normal(1)
        conditioningPDF = n1.computePDF([conditionalReferencePoint[0]])
        exact = conditionedPDF / conditioningPDF
        np.testing.assert_allclose(computed, exact)
        # CDF
        computed = conditionalDistribution.computeCDF([1.0, 1.0])
        print("computed CDF=", computed)
        exact = 0.7078609817371252
        np.testing.assert_allclose(computed, exact)
        # CDF when X0 = INF, X2 = INF
        computed = conditionalDistribution.computeCDF([7.0, 7.0])
        print("computed CDF=", computed)
        exact = 1.0
        np.testing.assert_allclose(computed, exact)

    def test_DrawPDF(self):
        # The random variable is (X0, X1, X2)
        distribution = ot.Normal(3)
        # We condition with respect to X1=mu1, i.e.
        # we consider (X0, X1, X2) | X1=2
        conditionalIndices = [1]
        conditionalReferencePoint = [2.0]
        conditionalDistribution = ot.Distribution(
            otbenchmark.ConditionalDistribution(
                distribution, conditionalIndices, conditionalReferencePoint
            )
        )
        # Avoid failing on CircleCi
        # _tkinter.TclError: no display name and no $DISPLAY environment variable
        try:
            graph = conditionalDistribution.drawPDF()
            _ = otv.View(graph)
        except Exception as e:
            print(e)

    def test_ConditionalDistribution2(self):
        # The random variable is (X0, X1, X2)
        distribution = ot.Normal(3)
        # We condition X = (X0, X1, X2) given X1=2.0, X2=3.0
        conditionalIndices = [1, 2]
        conditionalReferencePoint = [2.0, 3.0]
        for useIntegration in [True, False]:
            conditionalDistribution = ot.Distribution(
                otbenchmark.ConditionalDistribution(
                    distribution,
                    conditionalIndices,
                    conditionalReferencePoint,
                    useIntegration=useIntegration,
                )
            )
            # Configure tolerance depending on algorithm
            if useIntegration:
                rtol = 1.0e-7
            else:
                rtol = 1.0e-2
            # PDF
            computed = conditionalDistribution.computePDF([1.0])
            print("computed PDF=", computed)
            conditionedPDF = distribution.computePDF(
                [1.0, conditionalReferencePoint[0], conditionalReferencePoint[1]]
            )
            n2 = ot.Normal(2)
            conditioningPDF = n2.computePDF(
                [conditionalReferencePoint[0], conditionalReferencePoint[1]]
            )
            exact = conditionedPDF / conditioningPDF
            np.testing.assert_allclose(computed, exact)
            # CDF
            computed = conditionalDistribution.computeCDF([1.0])
            print("computed CDF=", computed)
            exact = 0.8413447460685339
            np.testing.assert_allclose(computed, exact, rtol=rtol)
            # CDF when X0 = INF, X2 = INF
            computed = conditionalDistribution.computeCDF([7.0])
            print("computed CDF=", computed)
            exact = 1.0
            np.testing.assert_allclose(computed, exact)

    def test_ConditionalDistribution3(self):
        # Do not condition anything.
        distribution = ot.Normal(3)
        conditionalIndices = []
        conditionalReferencePoint = []
        conditionalDistribution = ot.Distribution(
            otbenchmark.ConditionalDistribution(
                distribution, conditionalIndices, conditionalReferencePoint
            )
        )
        # PDF
        computed = conditionalDistribution.computePDF([1.0, 1.0, 1.0])
        print("computed PDF=", computed)
        exact = distribution.computePDF([1.0, 1.0, 1.0])
        np.testing.assert_allclose(computed, exact)
        # CDF
        computed = conditionalDistribution.computeCDF([1.0, 1.0, 1.0])
        print("computed CDF=", computed)
        exact = distribution.computeCDF([1.0, 1.0, 1.0])
        np.testing.assert_allclose(computed, exact)
        # CDF when X0 = INF, X2 = INF
        computed = conditionalDistribution.computeCDF([7.0, 7.0, 7.0])
        print("computed CDF=", computed)
        exact = 1.0
        np.testing.assert_allclose(computed, exact)

    def test_ConditionalDistribution4(self):
        # Create a dimension 5 distribution
        distribution = ot.Normal(5)
        conditionalIndices = [1, 2]
        conditionalReferencePoint = [2.0, 3.0]
        conditionalDistribution = ot.Distribution(
            otbenchmark.ConditionalDistribution(
                distribution, conditionalIndices, conditionalReferencePoint
            )
        )
        # PDF
        computed = conditionalDistribution.computePDF([1.0] * 3)
        print("computed PDF=", computed)


if __name__ == "__main__":
    unittest.main()
