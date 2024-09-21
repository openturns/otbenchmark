"""
RP75 analysis and 2D graphics
=============================
"""

# %%
# The objective of this example is to present problem 75 of the BBRC.
# We also present graphic elements for the visualization of the limit state surface in 2 dimensions.
#
# This problem has two dimension and a reference probability approximately equal to $10^{-2}$.
# Hence, the problem should be relatively easy to solve.
# The failure domain is made of two separate sub-domains, leading to two different design points.
# Hence, the FORM approximation cannot be accurate, because it systematically ignores one of them,
# no matter what point is found by the optimization algorithm.

# %%
import openturns as ot
import openturns.viewer as otv
import otbenchmark as otb

# %%
problem = otb.ReliabilityProblem75()
print(problem)

# %%
event = problem.getEvent()
g = event.getFunction()

# %%
problem.getProbability()

# %%
# Create the Monte-Carlo algorithm
algoProb = ot.ProbabilitySimulationAlgorithm(event)
algoProb.setMaximumOuterSampling(1000)
algoProb.setMaximumCoefficientOfVariation(0.01)
algoProb.run()

# %%
# Get the results
resultAlgo = algoProb.getResult()
neval = g.getEvaluationCallsNumber()
print("Number of function calls = %d" % (neval))
pf = resultAlgo.getProbabilityEstimate()
print("Failure Probability = %.4f" % (pf))
level = 0.95
c95 = resultAlgo.getConfidenceLength(level)
pmin = pf - 0.5 * c95
pmax = pf + 0.5 * c95
print("%.1f %% confidence interval :[%.4f,%.4f] " % (level * 100, pmin, pmax))

# %%
# Compute the bounds of the domain
# --------------------------------

# %%
inputVector = event.getAntecedent()
distribution = inputVector.getDistribution()
X1 = distribution.getMarginal(0)
X2 = distribution.getMarginal(1)
alphaMin = 0.00001
alphaMax = 1 - alphaMin
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
sampleSize = 5000
drawEvent = otb.DrawEvent(event)

# %%
cloud = drawEvent.drawSampleCrossCut(sampleSize)
_ = otv.View(cloud)

# %%
# Draw the limit state surface
# ----------------------------

# %%
bounds = ot.Interval(lowerBound, upperBound)
bounds

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
# Test with FORM method
# ---------------------

# %%
# We create a NearestPoint algorithm
nearestPointAlgorithm = ot.Cobyla()
# Resolution options:
eps = 1e-3
nearestPointAlgorithm.setMaximumCallsNumber(1000)
nearestPointAlgorithm.setMaximumAbsoluteError(eps)
nearestPointAlgorithm.setMaximumRelativeError(eps)
nearestPointAlgorithm.setMaximumResidualError(eps)
nearestPointAlgorithm.setMaximumConstraintError(eps)

# %%
initialNumberOfCall = g.getEvaluationCallsNumber()
mean = distribution.getMean()
algoFORM = ot.FORM(nearestPointAlgorithm, event, mean)
algoFORM.run()
resultFORM = algoFORM.getResult()
numberOfFunctionEvaluationsFORM = g.getEvaluationCallsNumber() - initialNumberOfCall
probabilityFORM = resultFORM.getEventProbability()
print("Number of calls to the limit state =", numberOfFunctionEvaluationsFORM)
print("Pf =", probabilityFORM)

# %%
# We create a NearestPoint algorithm
nearestPointAlgorithm = ot.AbdoRackwitz()
# Resolution options:
eps = 1e-3
nearestPointAlgorithm.setMaximumCallsNumber(100)
nearestPointAlgorithm.setMaximumAbsoluteError(eps)
nearestPointAlgorithm.setMaximumRelativeError(eps)
nearestPointAlgorithm.setMaximumResidualError(eps)
nearestPointAlgorithm.setMaximumConstraintError(eps)

# %%
# If the mean point is used as a starting point with the `AbdoRackwitz` class, then the algorithm fails with:
# ```
# RuntimeError: InternalException : Error in Abdo Rackwitz algorithm: the gradient of the level function is zero ...
# ```
# In order to fix this, we just use a different starting point.

# %%
startingPoint = mean + [1.0e-3] * 2

# %%
initialNumberOfCall = g.getEvaluationCallsNumber()
mean = distribution.getMean()
algoFORM = ot.FORM(nearestPointAlgorithm, event, startingPoint)
algoFORM.run()
resultFORM = algoFORM.getResult()
numberOfFunctionEvaluationsFORM = g.getEvaluationCallsNumber() - initialNumberOfCall
probabilityFORM = resultFORM.getEventProbability()
print("Number of calls to the limit state =", numberOfFunctionEvaluationsFORM)
print("Pf =", probabilityFORM)

# %%
mean

# %%
g.gradient(mean)

# %%
otv.View.ShowAll()
