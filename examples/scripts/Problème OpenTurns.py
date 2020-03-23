#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf8 -*-
import os
import time
import numpy as np
import math as m
import openturns as ot
import json
import requests


# In[2]:


from evaluate import evaluate


# In[3]:


username = 'testuser'
password = 'testpass'
set_id = -1
problem_id  = 2
def g_fun(x):
        #g_val_comp = evaluate(username, password, set_id, problem_id, x)
        g_val_sys, g_val_comp, msg = evaluate(username, password, set_id, problem_id, x)
        return g_val_comp


# In[4]:


x=[[0.545, 1.23],[ 0.7, 1],[0.545, 1.23]]


# In[5]:


start_time = time.time()
print(g_fun(x))
interval = time.time() - start_time
print ("Durée de la simulation :", round(interval, 2), "s")


# In[6]:


myFunction = ot.PythonFunction(2, 1, func_sample=g_fun)


# In[7]:


start_time = time.time()
print(myFunction(x))
interval = time.time() - start_time
print ("Durée de la simulation :", round(interval, 2), "s")


# In[ ]:


dist_X1 = ot.Normal(0., 1.)
dist_X2 = ot.Normal(0., 1.)
myDistribution = ot.ComposedDistribution([dist_X1, dist_X2])
myRandomVector = ot.RandomVector(myDistribution)


# In[ ]:


myFunction = ot.PythonFunction(2, 1, g_fun)
myOutputVector = ot.CompositeRandomVector(myFunction, myRandomVector)
#myOutputVector.getSample(10)


# In[ ]:


event = ot.Event(myOutputVector, ot.LessOrEqual(), 0.0)
# We create an OptimizationAlgorithm algorithm
solver = ot.SQP()
algo = ot.SORM(solver, event, [0.,0.])
algo.run()
result = algo.getResult()


# In[ ]:


print(result.getEventProbabilityBreitung(),
result.getEventProbabilityHohenBichler(),
result.getEventProbabilityTvedt())


# In[ ]:


optres = result.getOptimizationResult()
print(
"Design point:", optres.getOptimalPoint(),"\n" 
"Absolute error:", optres.getAbsoluteError(),"\n"#norme inifnie entre Xn et Xn+1
"Residual error:", optres.getResidualError() ,"\n" 
"Evaluation number:", optres.getEvaluationNumber())


# In[ ]:




