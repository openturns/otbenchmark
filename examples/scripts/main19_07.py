#!/usr/bin/env python

# -*- coding: utf8 -*-
import openturns as ot

from analytical_functions import gfun_8
from simulation_methods import run_MonteCarlo

# Distributions d'entrée
# ~ dist_X1 = ot.Normal(0., 1.)
# ~ dist_X2 = ot.Normal(0., 1.)
# ~ myDistribution = ot.ComposedDistribution([dist_X1, dist_X2])
parameters1 = ot.LogNormalMuSigma(120, 12, 0.0)
dist_X1 = ot.ParametrizedDistribution(parameters1)

parameters2 = ot.LogNormalMuSigma(120, 12, 0.0)
dist_X2 = ot.ParametrizedDistribution(parameters2)

parameters3 = ot.LogNormalMuSigma(120, 12, 0.0)
dist_X3 = ot.ParametrizedDistribution(parameters3)

parameters4 = ot.LogNormalMuSigma(120, 12, 0.0)
dist_X4 = ot.ParametrizedDistribution(parameters4)

parameters5 = ot.LogNormalMuSigma(50, 10, 0.0)
dist_X5 = ot.ParametrizedDistribution(parameters5)

parameters6 = ot.LogNormalMuSigma(40, 8, 0.0)
dist_X6 = ot.ParametrizedDistribution(parameters6)

myDistribution = ot.ComposedDistribution(
    [dist_X1, dist_X2, dist_X3, dist_X4, dist_X5, dist_X6]
)
myRandomVector = ot.RandomVector(myDistribution)

# Fonction
# ~ myFunction = ot.PythonFunction(2, 1, gfun_22)
myFunction = ot.PythonFunction(6, 1, gfun_8)


myOutputVector = ot.CompositeRandomVector(myFunction, myRandomVector)

# Evènement fiabiliste
event = ot.ThresholdEvent(myOutputVector, ot.LessOrEqual(), 0.0)

# ~ #Run FORM
# ~ FORM_result = run_FORM(event, myRandomVector, verbose=True,
#                          failure_domain=None)

# ~ #Run CMC

CMC_result = run_MonteCarlo(
    event,
    coefVar=0.01,
    outerSampling=3000,
    blockSize=100,
    verbose=True,
    failure_domain=None,
)
# ~ #Run Importance Sampling
# ~ IS_result = run_ImportanceSampling(event, pstar, sd=1., coefVar=0.01,
# ~ outerSampling=3000, blockSize=100, verbose=True, failure_domain=None)
# ~ #Run LHS
# ~ CMC_result = run_LHS(event, coefVar=0.01, outerSampling=3000,
#                        verbose=True, failure_domain=None)

# ~ #Run SubSet
# ~ CMC_result = run_SubSet(event, coefVar=0.01, outerSampling=3000,
#                           verbose=True, failure_domain=None)

"""
TO DO LIST :
phase 1
- (ajouter SORM)
- ajouter le strong maximum test avec une fonction paramétrique
  qui ressort "P* est unique" ou non
- sortir un df avec les bons indicateurs pour chaque méthode
phase 2
- créer un métamodel de krigeage sur G
- faire un AK-MCS à la mano ?

"""
