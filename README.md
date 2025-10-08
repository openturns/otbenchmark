[![GHA](https://github.com/openturns/otbenchmark/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/openturns/otbenchmark/actions/workflows/build.yml)

# otbenchmark

## What is it?

The goal of this project is to provide benchmark classes for OpenTURNS. 
It provides a framework to create use-cases which are associated with
reference values.
Such a benchmark problem may be used in order to check that a given
algorithm works as expected and to measure its performance in terms 
of accuracy and speed.

Two categories of benchmark classes are currently provided:
* reliability problems, i.e. estimating the probability that 
the output of a function is less than a threshold,
* sensitivity problems, i.e. estimating sensitivity indices, 
for example Sobol' indices.

Most of the reliability problems were adapted from the RPRepo

https://rprepo.readthedocs.io/en/latest/

This module makes it possible to create a problem, run an algorithm and 
compare the computed probability with a reference probability. 
Moreover, we can loop over all problems and run several methods on these 
problems.

## Example
The next example shows how to use the R-S reliability problem.
```python
import otbenchmark as otb
import openturns as ot

problem = otb.RminusSReliability()
event = problem.getEvent()
reference_pf = problem.getProbability() # exact probability
# Create the Monte-Carlo algorithm
algoProb = ot.ProbabilitySimulationAlgorithm(event)
algoProb.setMaximumOuterSampling(1000)
algoProb.setMaximumCoefficientOfVariation(0.01)
algoProb.run()
resultAlgo = algoProb.getResult()
computed_pf = resultAlgo.getProbabilityEstimate()
absoluteError = abs(computed_pf - reference_pf)
```

## Authors

* Michaël Baudin
* Youssef Jebroun
* Elias Fekhari
* Vincent Chabridon

## Installation

To install the module, we can use either pip or conda: 

```
pip install otbenchmark
```

## Documentation

The documentation is available here: https://openturns.github.io/otbenchmark/master/

