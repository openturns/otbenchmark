"""
Print the sensitivity analysis problems
=======================================
"""

# %%
# In this example, we show how to print all the sensitivity analysis problems.

# %%
import otbenchmark as otb
import pandas as pd

# %%
# We import the list of problems.
benchmarkProblemList = otb.SensitivityBenchmarkProblemList()
numberOfProblems = len(benchmarkProblemList)
print(numberOfProblems)

# %%
# For each problem in the benchmark, print the problem name and the exact Sobol' indices.
for i in range(numberOfProblems):
    problem = benchmarkProblemList[i]
    name = problem.getName()
    first_order_indices = problem.getFirstOrderIndices()
    total_order_indices = problem.getTotalOrderIndices()
    dimension = problem.getInputDistribution().getDimension()
    print(
        "#",
        i,
        ":",
        name,
        " : S = ",
        first_order_indices,
        "T=",
        total_order_indices,
        ", dimension=",
        dimension,
    )

# %%
problem_names = [
    benchmarkProblem.getName() for benchmarkProblem in benchmarkProblemList
]
columns = ["$d$"]
df_problems_list = pd.DataFrame(index=problem_names, columns=columns)
for problem in benchmarkProblemList:
    name = problem.getName()
    d = problem.getInputDistribution().getDimension()
    df_problems_list.loc[name] = [int(d)]
print(df_problems_list)

# %%
latex_code = df_problems_list.to_latex()
# text_file = open("sensitivity_problems_list.tex", "w")
# text_file.write(latex_code)
# text_file.close()
