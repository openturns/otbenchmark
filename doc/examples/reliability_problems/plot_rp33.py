"""
RP33 analysis and 2D graphics
=============================
"""

# %%
# The objective of this example is to present problem 33 of the BBRC.

# %%
import otbenchmark as otb

# %%
problem = otb.ReliabilityProblem33()
print(problem)


# %%
event = problem.getEvent()
g = event.getFunction()


# %%
problem.getProbability()


# %%
inputVector = event.getAntecedent()
distribution = inputVector.getDistribution()


# %%
inputDimension = distribution.getDimension()
inputDimension


# %%
alpha = 1 - 0.00001
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
# Plot cross-cuts of the distribution
# -----------------------------------

# %%
crossCut = otb.CrossCutDistribution(distribution)

# %%
_ = crossCut.drawMarginalPDF()

# %%
inputVector = event.getAntecedent()
event = problem.getEvent()
g = event.getFunction()

# %%
sampleSize = 5000
sampleInput = inputVector.getSample(sampleSize)
sampleOutput = g(sampleInput)
drawEvent = otb.DrawEvent(event)

# %%
_ = drawEvent.drawLimitState(bounds)

# %%
sampleSize = 500
_ = drawEvent.drawSample(sampleSize)

# %%
_ = drawEvent.fillEvent(bounds)
