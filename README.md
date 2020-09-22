[![CircleCI](https://circleci.com/gh/mbaudin47/otbenchmark.svg?style=svg)](https://circleci.com/gh/mbaudin47/otbenchmark)

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

Most of the reliability problems were adapted from the RPRepo :

https://rprepo.readthedocs.io/en/latest/

This module allows you to create a problem, run an algorithm and 
compare the computed probability with a reference probability: 

```
problem = otb.RminusSReliability()
event = problem.getEvent()
pfReference = problem.getProbability() # exact probability
# Create the Monte-Carlo algorithm
algoProb = ot.ProbabilitySimulationAlgorithm(event)
algoProb.setMaximumOuterSampling(1000)
algoProb.setMaximumCoefficientOfVariation(0.01)
algoProb.run()
resultAlgo = algoProb.getResult()
pf = resultAlgo.getProbabilityEstimate()
absoluteError = abs(pf - pfReference)
```

Moreover, we can loop over all problems and run several methods on these 
problems.

## Authors

Michaël Baudin
Youssef Jebroun
Elias Fekhari
Vincent Chabridon

## Overview of the benchmark problems

* The FORM algorithm does not perform correctly on: RP75, RP111
and Four-branch serial system.
An explanation would be required for this.

* The computeCDF() method does not perform correctly on many problems.
An explanation would be required for this.

