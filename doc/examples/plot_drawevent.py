"""
Demonstration of the DrawEvent class
====================================
"""

import otbenchmark as otb
import openturns.viewer as otv

# %%
# 3D problem
# ----------

# %%
problem = otb.ReliabilityProblem33()

# %%
event = problem.getEvent()
g = event.getFunction()

# %%
inputVector = event.getAntecedent()
distribution = inputVector.getDistribution()

# %%
inputDimension = distribution.getDimension()
inputDimension

# %%
alpha = 1 - 0.00001

# %%
bounds, marginalProb = distribution.computeMinimumVolumeIntervalWithMarginalProbability(
    alpha
)

# %%
referencePoint = distribution.getMean()
referencePoint

# %%
inputVector = event.getAntecedent()
event = problem.getEvent()
g = event.getFunction()

# %%
drawEvent = otb.DrawEvent(event)

# %%
# The highest level method is the `draw` method which flags allow to gather various graphics into a single one.
_ = drawEvent.draw(bounds)

# %%
_ = drawEvent.draw(bounds, fillEvent=True)

# %%
# The `drawLimitState` method only draws the limit state.
_ = drawEvent.drawLimitState(bounds)

# %%
# The `drawSample` method plots a sample with a color code which specifies which points are inside or outside the event.
sampleSize = 500
_ = drawEvent.drawSample(sampleSize)

# %%
_ = drawEvent.fillEvent(bounds)

# %%
# 2D problem
# ----------
#
# When the problem has 2 dimensions, single cross-cuts are sufficient.
# This is why we use the `*CrossCut` methods.

# %%
problem = otb.ReliabilityProblem22()

# %%
event = problem.getEvent()
g = event.getFunction()

# %%
inputVector = event.getAntecedent()
distribution = inputVector.getDistribution()
bounds, marginalProb = distribution.computeMinimumVolumeIntervalWithMarginalProbability(
    1.0 - 1.0e-6
)

# %%
sampleSize = 10000
drawEvent = otb.DrawEvent(event)

# %%
cloud = drawEvent.drawSampleCrossCut(sampleSize)
_ = otv.View(cloud)

# %%
graph = drawEvent.drawLimitStateCrossCut(bounds)
graph.add(cloud)
_ = otv.View(graph)

# %%
domain = drawEvent.fillEventCrossCut(bounds)
_ = otv.View(domain)

# %%
domain.add(cloud)
_ = otv.View(domain)

# %%
# For a 2D sample, it is sometimes handy to re-use a precomputed sample.
# In this case, we can use the `drawInputOutputSample` method.
inputSample = distribution.getSample(sampleSize)
outputSample = g(inputSample)
drawEvent.drawInputOutputSample(inputSample, outputSample)

# %%
otv.View.ShowAll()
