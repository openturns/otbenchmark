# -*- coding: utf-8 -*-
"""
Test for BBRCDistribution class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot


class CheckBBRCDistribution(unittest.TestCase):
    def test_BBRCDistribution(self):
        my_dist = otb.BBRCDistribution(-1, 1)

        # Check the distribution with a CDF value
        exact_dist = ot.ComposedDistribution(
            [
                ot.ParametrizedDistribution(ot.LogNormalMuSigma(120, 12)),
                ot.ParametrizedDistribution(ot.LogNormalMuSigma(120, 12)),
                ot.ParametrizedDistribution(ot.LogNormalMuSigma(120, 12)),
                ot.ParametrizedDistribution(ot.LogNormalMuSigma(120, 12)),
                ot.ParametrizedDistribution(ot.LogNormalMuSigma(50, 10)),
                ot.ParametrizedDistribution(ot.LogNormalMuSigma(40, 8)),
            ]
        )
        exact_cdf_value = exact_dist.computeCDF([150] * 6)
        inputDistribution = my_dist.build_composed_dist()
        tested_cdf_value = inputDistribution.computeCDF([150] * 6)
        np.testing.assert_allclose(exact_cdf_value, tested_cdf_value, rtol=1.0e-15)


if __name__ == "__main__":
    unittest.main()
