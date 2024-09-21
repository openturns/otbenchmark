"""
RP28 analysis and 2D graphics
=============================
"""

# %%
# The objective of this example is to present problem 28 of the BBRC.
# We also present graphic elements for the visualization of the limit state surface in 2 dimensions.

# %%
import openturns as ot
import openturns.viewer as otv
import otbenchmark as otb


# %%
problem = otb.ReliabilityProblem28()


# %%
print(problem)


# %%
event = problem.getEvent()
g = event.getFunction()


# %%
problem.getProbability()


# %%
# Create the Monte-Carlo algorithm
algoProb = ot.ProbabilitySimulationAlgorithm(event)
algoProb.setMaximumOuterSampling(10000)
algoProb.setBlockSize(128)
algoProb.setMaximumCoefficientOfVariation(0.01)
algoProb.run()


# %%
# Get the results
resultAlgo = algoProb.getResult()
neval = g.getEvaluationCallsNumber()
print("Number of function calls = %d" % (neval))
pf = resultAlgo.getProbabilityEstimate()
print("Failure Probability = %.4f (* 1.e-7)" % (pf * 1.0e7))
level = 0.95
c95 = resultAlgo.getConfidenceLength(level)
pmin = pf - 0.5 * c95
pmax = pf + 0.5 * c95
print(
    "%.1f %% confidence interval :[%.4f,%.4f] * 1.e-7 "
    % (level * 100, pmin * 1.0e7, pmax * 1.0e7)
)

# %%
# Compute the bounds of the domain
# --------------------------------

# %%
inputVector = event.getAntecedent()
distribution = inputVector.getDistribution()
X1 = distribution.getMarginal(0)
X2 = distribution.getMarginal(1)
alphaMin = 1.0e-8
alphaMax = 1.0 - alphaMin
lowerBound = ot.Point(
    [X1.computeQuantile(alphaMin)[0], X2.computeQuantile(alphaMin)[0]]
)
upperBound = ot.Point(
    [X1.computeQuantile(alphaMax)[0], X2.computeQuantile(alphaMax)[0]]
)


# %%
nbPoints = [100, 100]
figure = g.draw(lowerBound, upperBound, nbPoints)
figure.setTitle("Iso-values of limit state function")
_ = otv.View(figure)

# %%
# Print the iso-values of the distribution
# ----------------------------------------

# %%
_ = otv.View(distribution.drawPDF())


# %%
sampleSize = 100000
drawEvent = otb.DrawEvent(event)

# %%
cloud = drawEvent.drawSampleCrossCut(sampleSize)
_ = otv.View(cloud)

# %%
# Draw the limit state surface
# ----------------------------

# %%
bounds = ot.Interval(lowerBound, upperBound)

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
otv.View.ShowAll()
