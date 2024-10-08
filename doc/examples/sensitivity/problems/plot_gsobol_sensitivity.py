"""
Benchmark the G-Sobol test function
===================================
"""

# %%
import openturns as ot
import otbenchmark as otb
import openturns.viewer as otv

# %%
problem = otb.GSobolSensitivity()
print(problem)

# %%
distribution = problem.getInputDistribution()
model = problem.getFunction()

# %%
# Exact first and total order
exact_first_order = problem.getFirstOrderIndices()
exact_first_order

# %%
exact_total_order = problem.getTotalOrderIndices()
print(exact_total_order)

# %%
# Plot function
# -------------

# %%
# Create X/Y data
ot.RandomGenerator.SetSeed(0)
size = 200
inputDesign = ot.MonteCarloExperiment(distribution, size).generate()
outputDesign = model(inputDesign)

# %%
dimension = distribution.getDimension()
full_sample = ot.Sample(size, 1 + dimension)
full_sample[:, range(dimension)] = inputDesign
full_sample[:, dimension] = outputDesign
full_description = list(inputDesign.getDescription())
full_description.append(outputDesign.getDescription()[0])
full_sample.setDescription(full_description)

# %%
marginal_distribution = ot.ComposedDistribution(
    [
        ot.KernelSmoothing().build(full_sample.getMarginal(i))
        for i in range(1 + dimension)
    ]
)
clouds = ot.VisualTest.DrawPairsMarginals(full_sample, marginal_distribution)
_ = otv.View(clouds, figure_kw={"figsize": (6.0, 6.0)})


# %%
# Create X/Y data
ot.RandomGenerator.SetSeed(0)
size = 1000
inputDesign = ot.MonteCarloExperiment(distribution, size).generate()
outputDesign = model(inputDesign)

# %%
output_distribution = ot.KernelSmoothing().build(outputDesign)
_ = otv.View(output_distribution.drawPDF())

# %%
# Perform SA
# ----------

# %%
# Create X/Y data
ot.RandomGenerator.SetSeed(0)
size = 10000
inputDesign = ot.SobolIndicesExperiment(distribution, size).generate()
outputDesign = model(inputDesign)

# %%
# Compute first order indices using the Saltelli estimator
sensitivityAnalysis = ot.SaltelliSensitivityAlgorithm(inputDesign, outputDesign, size)
computed_first_order = sensitivityAnalysis.getFirstOrderIndices()
computed_total_order = sensitivityAnalysis.getTotalOrderIndices()

# %%
# Compare with exact results
print("Sample size : ", size)
# First order
# Compute absolute error (the LRE cannot be computed,
# because S can be zero)
print("Computed first order = ", computed_first_order)
print("Exact first order = ", exact_first_order)
# Total order
print("Computed total order = ", computed_total_order)
print("Exact total order = ", exact_total_order)

# %%
_ = otv.View(sensitivityAnalysis.draw())

# %%
otv.View.ShowAll()
