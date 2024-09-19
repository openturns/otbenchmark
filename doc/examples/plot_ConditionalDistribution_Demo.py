"""
Conditional distributions
=========================
"""

# %%
# Conditioning is a way to reduce the dimensionnality of a multivariate distribution.

# %%
import openturns as ot
import otbenchmark as otb
import openturns.viewer as otv

# %%
# Conditional distribution of a three dimensional gaussian distribution
# ---------------------------------------------------------------------

# %%
# The random variable is (X0, X1, X2).
distribution = ot.Normal(3)

# %%
# We condition with respect to X1=mu1, i.e. we consider (X0, X1, X2) | X1=2.
conditionalIndices = [1]
conditionalReferencePoint = [2.0]
conditionalDistribution = ot.Distribution(
    otb.ConditionalDistribution(
        distribution, conditionalIndices, conditionalReferencePoint
    )
)


# %%
_ = otv.View(conditionalDistribution.drawPDF())

# %%
# Conditional distribution of a three dimensional mixture
# -------------------------------------------------------

# %%
# Create a Funky distribution
corr = ot.CorrelationMatrix(3)
corr[0, 1] = 0.2
copula = ot.NormalCopula(corr)
x1 = ot.Normal(-1.0, 1.0)
x2 = ot.Normal(2.0, 1.0)
x3 = ot.Normal(1.0, 1.0)
x_funk = ot.ComposedDistribution([x1, x2, x3], copula)


# %%
# Create a Punk distribution
x1 = ot.Normal(1.0, 1.0)
x2 = ot.Normal(-2, 1.0)
x3 = ot.Normal(2.0, 1.0)
x_punk = ot.ComposedDistribution([x1, x2, x3], copula)


# %%
distribution = ot.Mixture([x_funk, x_punk], [0.5, 1.0])


# %%
referencePoint = distribution.getMean()
referencePoint


# %%
conditionalIndices = [1]
conditionalReferencePoint = [-0.5]
conditionalDistribution = ot.Distribution(
    otb.ConditionalDistribution(
        distribution, conditionalIndices, conditionalReferencePoint
    )
)


# %%
_ = otv.View(conditionalDistribution.drawPDF())

# %%
otv.View.ShowAll()
