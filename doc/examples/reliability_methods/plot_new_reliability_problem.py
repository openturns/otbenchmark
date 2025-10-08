"""
Create a new reliability problem
================================
"""

# %%
# The objective of this example is to create a new reliability
# problem.
# This can be useful when we want to consider a new problem which is
# not already available in the benchmark.
# This makes it possible to consider a new problem as if it was in the
# package.

# %%
import openturns as ot
import openturns.viewer as otv
import otbenchmark as otb
import numpy as np


# %%
# In order to create our own benchmark problem, we must
# create a new class which derives from ReliabilityBenchmarkProblem.
class OscillatorProblem(otb.ReliabilityBenchmarkProblem):
    def __init__(self):
        """Create the Oscillator problem

        This is a two-degree-of-freedom damped oscillator with primary
        and secondary systems.

        Reference
        ---------
        - "Analyse de sensibilité fiabiliste avec prise en compte d'incertitudes
          sur le modèle probabiliste", Vincent Chabridon. Thèse. 2018, pp.91-92.
        - De Stefano M., Der Kiureghian A. (1990). An efficient algorithm for
          second-order reliability analysis.
          Report No. UCB/SEMM-90/20. Dept of Civil and Environmental Engineering,
          University of California, Berkeley.
        """

        def oscillator(x):
            mp, ms, kp, ks, xip, xis, S0 = x
            omega_p = np.sqrt(kp / mp)
            omega_s = np.sqrt(ks / ms)
            gamma = ms / mp
            omega_a = 0.5 * (omega_p + omega_s)
            xi_a = 0.5 * (xip + xis)
            theta = 1.0 / omega_a * (omega_p - omega_s)
            factor_1 = np.pi * S0 / (4.0 * xis * omega_s**3)
            factor_2 = (
                xi_a * xis / (xip * xis * (4.0 * xi_a**2 + theta**2) + gamma * xi_a**2)
            )
            factor_3 = (
                (xip * omega_p**3 + xis * omega_s**3)
                * omega_p
                / (4.0 * xi_a * omega_a**4)
            )
            F = 3 * ks * np.sqrt(factor_1 * factor_2 * factor_3)
            return [F]

        name = "Oscillator"
        dim = 7
        limitStateFunction = ot.PythonFunction(dim, 1, oscillator)
        mean_list = [1.5, 0.01, 1.0, 0.01, 0.05, 0.02, 100.0]
        cov_list = [0.1, 0.1, 0.2, 0.2, 0.4, 0.5, 0.1]
        myCollection = ot.DistributionCollection(dim)
        for i, (mu, cov) in enumerate(zip(mean_list, cov_list)):
            parameters = ot.LogNormalMuSigma(mu, mu * cov, 0.0)
            myCollection[i] = ot.ParametrizedDistribution(parameters)
        distribution = ot.ComposedDistribution(myCollection)
        inputRandomVector = ot.RandomVector(distribution)
        outputRandomVector = ot.CompositeRandomVector(
            limitStateFunction, inputRandomVector
        )
        threshold = 0.0
        thresholdEvent = ot.ThresholdEvent(outputRandomVector, ot.Less(), threshold)
        probability = 3.78e-7
        super().__init__(name, thresholdEvent, probability)
        return None


# %%
problem = OscillatorProblem()
print(problem)

# %%
event = problem.getEvent()
g = event.getFunction()

# %%
problem.getProbability()

# %%
# Create the Monte-Carlo algorithm
algoProb = ot.ProbabilitySimulationAlgorithm(event)
algoProb.setMaximumOuterSampling(100)
algoProb.setBlockSize(10)
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
# The reference probability is too close to zero: Monte-Carlo sampling cannot
# achieve a satisfactory accuracy.

# %%
otv.View.ShowAll()

# %%
