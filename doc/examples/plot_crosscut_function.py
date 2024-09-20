"""
Draw cross-cuts of multidimensional functions
=============================================
"""

# %%
# This example shows how to represent multidimensional functions.
# When 2D plots are to draw, contours are used.
# We use 2D cross-sections to represent multidimensional objects when required,
# which leads to cross-cuts representations.
#

# %%
import otbenchmark as otb
import openturns.viewer as otv


# %%
problem = otb.ReliabilityProblem33()

# %%
event = problem.getEvent()
g = event.getFunction()

# %%
# Compute the bounds of the domain
# --------------------------------

# %%
inputVector = event.getAntecedent()
distribution = inputVector.getDistribution()


# %%
inputDimension = distribution.getDimension()
inputDimension


# %%
alpha = 1 - 1.0e-5
bounds, marginalProb = distribution.computeMinimumVolumeIntervalWithMarginalProbability(
    alpha
)


# %%
referencePoint = distribution.getMean()
referencePoint


# %%
crossCut = otb.CrossCutFunction(g, referencePoint)
_ = crossCut.draw(bounds)


# %%
# Let us explain this figure in detail, by describing each sub-plot from top to bottom,
# and from left to right:
#
# * Fig. A,
# * Fig. B, C,
# * Fig. D, E, F.
#
# Let :math:`\bar{x}\in\mathbb{R}^3` be the reference point.
#
# * Fig. A : represents :math:`y=f(x_1, \bar{x}_2, \bar{x}_3)`,
#   which is a function depending on :math:`x_1` only.
# * Fig. B : represents the contours of the bi-dimensional function
#   :math:`y=f(x_1, x_2, \bar{x}_3)`
#   which depends on :math:`x_1` and :math:`x_2`.
# * Fig. C : represents :math:`y=f(\bar{x}_1, x_2, \bar{x}_3)`,
#   which is a function depending on :math:`x_2` only.
# * Fig. D : represents the contours of the bi-dimensional function
#   :math:`y=f(x_1, \bar{x}_2, x_3)`
#   which depends on :math:`x_1` and :math:`x_3`.
# * Fig. E : represents the contours of the bi-dimensional function
#   :math:`y=f(\bar{x}_1, x_2, x_3)`
#   which depends on :math:`x_2` and :math:`x_3`.
# * Fig. F : represents :math:`y=f(\bar{x}_1, \bar{x}_2, x_3)`,
#   which is a function depending on :math:`x_3` only.
#

# %%
otv.View.ShowAll()
