# Copyright 2020 EDF.
"""
Test for ConditionalDistribution class.
"""
import otbenchmark
import unittest
import openturns as ot


class CheckCrossCutDistribution(unittest.TestCase):
    def test_CrossCutDistribution(self):
        distribution = ot.Normal(2)
        referencePoint = distribution.getMean()
        crossCut = otbenchmark.CrossCutDistribution(distribution)
        # Avoid failing on CircleCi
        # _tkinter.TclError: no display name and no $DISPLAY environment variable
        try:
            _ = crossCut.drawMarginalPDF()
            _ = crossCut.drawConditionalPDF(referencePoint)
        except Exception as e:
            print(e)

    def test_CrossCutDistribution2(self):
        # Create a Funky distribution
        corr = ot.CorrelationMatrix(2)
        corr[0, 1] = 0.2
        copula = ot.NormalCopula(corr)
        x1 = ot.Normal(-1.0, 1.0)
        x2 = ot.Normal(2.0, 1.0)
        x_funk = ot.ComposedDistribution([x1, x2], copula)
        # Create a Punk distribution
        x1 = ot.Normal(1.0, 1.0)
        x2 = ot.Normal(-2.0, 1.0)
        x_punk = ot.ComposedDistribution([x1, x2], copula)
        distribution = ot.Mixture([x_funk, x_punk], [0.5, 1.0])
        referencePoint = distribution.getMean()
        crossCut = otbenchmark.CrossCutDistribution(distribution)
        # Avoid failing on CircleCi
        # _tkinter.TclError: no display name and no $DISPLAY environment variable
        try:
            _ = crossCut.drawMarginalPDF()
            _ = crossCut.drawConditionalPDF(referencePoint)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    import matplotlib

    matplotlib.use("Agg")
    unittest.main()
