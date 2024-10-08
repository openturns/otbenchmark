"""
RP55 analysis and 2D graphics
=============================
"""

# %%
# The objective of this example is to present problem 55 of the BBRC.
# We also present graphic elements for the visualization of the limit state surface in 2 dimensions.
#
# The dimension is equal to 2 and the probability is close to $10^{-2}$.
# This makes this problem relatively easy to solve.
# The distribution is uniform in the square $[-1,1]^2$.
# The failure domain is made of 5 diagonal bands.
# Capturing these bands is relatively easy and a Monte-Carlo simulation perform well in this case.
# The FORM method cannot perform correctly, since the failure domain cannot be linearized in the gaussian space.
# Hence, the SORM or FORM-IS methods do not perform satisfactorily.

# %%
import openturns as ot
import otbenchmark as otb
import openturns.viewer as otv

# %%
# Disable warnings
ot.Log.Show(ot.Log.NONE)

# %%
problem = otb.ReliabilityProblem55()
print(problem)

# %%
event = problem.getEvent()
g = event.getFunction()

# %%
problem.getProbability()

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
# Plot the iso-values of the distribution
# ----------------------------------------

# %%
_ = otv.View(distribution.drawPDF())


# %%
sampleSize = 5000
sampleInput = inputVector.getSample(sampleSize)
sampleOutput = g(sampleInput)
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
# Perform Monte-Carlo simulation
# ------------------------------

# %%
algoProb = ot.ProbabilitySimulationAlgorithm(event)
algoProb.setMaximumOuterSampling(1000)
algoProb.setMaximumCoefficientOfVariation(0.01)
algoProb.run()


# %%
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
# With FORM-IS
# ------------

# %%
maximumEvaluationNumber = 1000
maximumAbsoluteError = 1.0e-3
maximumRelativeError = 1.0e-3
maximumResidualError = 1.0e-3
maximumConstraintError = 1.0e-3
nearestPointAlgorithm = ot.AbdoRackwitz()
nearestPointAlgorithm.setMaximumCallsNumber(maximumEvaluationNumber)
nearestPointAlgorithm.setMaximumAbsoluteError(maximumAbsoluteError)
nearestPointAlgorithm.setMaximumRelativeError(maximumRelativeError)
nearestPointAlgorithm.setMaximumResidualError(maximumResidualError)
nearestPointAlgorithm.setMaximumConstraintError(maximumConstraintError)


# %%
metaAlgorithm = otb.ReliabilityBenchmarkMetaAlgorithm(problem)
benchmarkResult = metaAlgorithm.runFORMImportanceSampling(
    nearestPointAlgorithm, maximumOuterSampling=10 ** 5, coefficientOfVariation=0.0
)


# %%
print(benchmarkResult.summary())

# %%
# With Quasi-Monte-Carlo
# ----------------------

# %%
sequence = ot.SobolSequence()
experiment = ot.LowDiscrepancyExperiment(sequence, 1)
experiment.setRandomize(False)


# %%
algo = ot.ProbabilitySimulationAlgorithm(event, experiment)
algo.setMaximumOuterSampling(10 ** 3)
algo.setMaximumCoefficientOfVariation(0.0)
algo.setBlockSize(10 ** 3)
algo.run()


# %%
result = algo.getResult()
probability = result.getProbabilityEstimate()
print("Pf=", probability)

# %%
otv.View.ShowAll()
