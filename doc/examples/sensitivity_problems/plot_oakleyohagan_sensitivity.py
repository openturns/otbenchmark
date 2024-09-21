"""
Benchmark the Oakley-O'Hagan test function
==========================================
"""

# %%
import openturns as ot
import otbenchmark as otb
import openturns.viewer as otv

# %%
problem = otb.OakleyOHaganSensitivity()
print(problem)

# %%
distribution = problem.getInputDistribution()
model = problem.getFunction()

# %%
# Exact first and total order
exact_first_order = problem.getFirstOrderIndices()
print(exact_first_order)

# %%
exact_total_order = problem.getTotalOrderIndices()
print(exact_total_order)

# %%
# Plot the function
# -----------------

# %%
# Create X/Y data
ot.RandomGenerator.SetSeed(0)
size = 200
inputDesign = ot.MonteCarloExperiment(distribution, size).generate()
outputDesign = model(inputDesign)

# %%
dimension = distribution.getDimension()
nbcolumns = 5
nbrows = int(dimension / nbcolumns)
grid = ot.GridLayout(nbrows, nbcolumns)
inputDescription = distribution.getDescription()
outputDescription = model.getOutputDescription()[0]
index = 0
for i in range(nbrows):
    for j in range(nbcolumns):
        graph = ot.Graph(
            "n=%d" % (size), inputDescription[index], outputDescription, True, ""
        )
        sample = ot.Sample(size, 2)
        sample[:, 0] = inputDesign[:, index]
        sample[:, 1] = outputDesign[:, 0]
        cloud = ot.Cloud(sample)
        graph.add(cloud)
        grid.setGraph(i, j, graph)
        index += 1
_ = otv.View(grid, figure_kw={"figsize": (10.0, 10.0)})

# %%
output_distribution = ot.KernelSmoothing().build(outputDesign)
_ = otv.View(output_distribution.drawPDF())

# %%
# Perform sensitivity analysis
# ----------------------------

# %%
# Create X/Y data
ot.RandomGenerator.SetSeed(0)
size = 1000
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
