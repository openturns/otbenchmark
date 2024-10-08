"""
Problem RP8
===========
"""

# %%
# In this example, we present the RP8 problem of BBRC 2019 using the FORM SORM method and the Monte Carlo method.

# %%
import otbenchmark as otb
import matplotlib.pyplot as plt

# %%
problem = otb.ReliabilityProblem8()
print(problem)

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
print(inputDimension)

# %%
alpha = 1.0 - 1.0e-5
bounds, marginalProb = distribution.computeMinimumVolumeIntervalWithMarginalProbability(
    alpha
)

# %%
referencePoint = distribution.getMean()
print(referencePoint)

# %%
crossCut = otb.CrossCutFunction(g, referencePoint)
fig = crossCut.draw(bounds)
# Remove the legend labels because there
# are too many for such a small figure
for ax in fig.axes:
    ax.legend("")
# Increase space between sub-figures so that
# there are no overlap
plt.subplots_adjust(hspace=0.5, wspace=0.75)

# %%
# Plot cross-cuts of the distribution
# -----------------------------------

# %%
crossCut = otb.CrossCutDistribution(distribution)

# %%
fig = crossCut.drawMarginalPDF()
# Remove the legend labels because there
# are too many for such a small figure
for ax in fig.axes:
    ax.legend("")
# Increase space between sub-figures so that
# there are no overlap
plt.subplots_adjust(hspace=0.5, wspace=0.75)

# %%
# The correct way to represent cross-cuts of a distribution is to draw the contours
# of the PDF of the conditional distribution.

# %%
fig = crossCut.drawConditionalPDF(referencePoint)
# Remove the legend labels because there
# are too many for such a small figure
for ax in fig.axes:
    ax.legend("")
# Increase space between sub-figures so that
# there are no overlap
plt.subplots_adjust(hspace=0.5, wspace=0.75)

# %%
inputVector = event.getAntecedent()
event = problem.getEvent()
g = event.getFunction()

# %%
drawEvent = otb.DrawEvent(event)

# %%
_ = drawEvent.draw(bounds)
# Increase space between sub-figures so that
# there are no overlap
plt.subplots_adjust(hspace=0.5, wspace=0.75)
