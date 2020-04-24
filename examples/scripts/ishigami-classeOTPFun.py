# -*- coding: utf-8 -*-

# Pour OT v1.1

import openturns as ot
from math import sin, pi, sqrt


# A parametrized class
class IshigamiFunction(ot.OpenTURNSPythonFunction):
    def __init__(self, a, b):
        super(IshigamiFunction, self).__init__(3, 1)
        self._a = a
        self._b = b

    def _exec(self, X):
        y = sin(X[0]) + self._a * sin(X[1]) ** 2 + self._b * X[2] ** 4 * sin(X[0])
        return [y]


a = 7.0
b = 0.1
myParametricWrapper = IshigamiFunction(a, b)
myWrapper = ot.Function(myParametricWrapper)

# Create the marginal distributions
distributionX0 = ot.Uniform(-pi, pi)
distributionX1 = ot.Uniform(-pi, pi)
distributionX2 = ot.Uniform(-pi, pi)

# Create the input probability distribution
inputDistribution = ot.ComposedDistribution(
    (distributionX0, distributionX1, distributionX2)
)

# Create the input random vector
inputRandomVector = ot.RandomVector(inputDistribution)

# Create the output variable of interest
outputVariableOfInterest = ot.RandomVector(myWrapper, inputRandomVector)

# Start the simulations
outputSample = outputVariableOfInterest.getSample(1000)

# Get the empirical mean and standard deviations
empiricalMean = outputSample.computeMean()
empiricalSd = outputSample.computeStandardDeviationPerComponent()
print("Mean=%f, Sd.Dev.=%f" % (empiricalMean[0], empiricalSd[0]))

mu = a / 2.0
varY = 1.0 / 2.0 + a ** 2 / 8 + b * pi ** 4 / 5 + b ** 2 * pi ** 8 / 18
sigma = sqrt(varY)
print("Exact Mean=", mu, ", Exact St.Dev=", sigma)
