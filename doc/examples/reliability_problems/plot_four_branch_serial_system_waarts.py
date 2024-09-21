"""
Using the Waarts four-branch serial system
==========================================
"""

# %%
# References
# ----------
#
# * Waarts, P.-H. (2000). Structural reliability using finite element
#   methods: an appraisal of DARS: Directional Adaptive Response Surface
#   Sampling. Ph. D. thesis, Technical University of Delft, The Netherlands.
#   Pages 58, 69, 160.
#
# * Thèse Vincent Dubourg 2011, Méta-modèles adaptatifs pour l’analyse
#   de fiabilité et l’optimisation sous contrainte fiabiliste,
#   section "A two-dimensional four-branch serial system", page 182
#

# %%
import openturns as ot
import openturns.viewer as otv
import otbenchmark as otb

# %%
problem = otb.FourBranchSerialSystemReliability()

# %%
event = problem.getEvent()
g = event.getFunction()

# %%
inputVector = event.getAntecedent()
distribution = inputVector.getDistribution()

# %%
# Draw isolines
lowerBound = ot.Point([-5.0, -5.0])
upperBound = ot.Point([5.0, 5.0])
nbPoints = [100, 100]
_ = otv.View(g.draw(lowerBound, upperBound, nbPoints))


# %%
sampleSize = 500

# %%
drawEvent = otb.DrawEvent(event)

# %%
cloud = drawEvent.drawSampleCrossCut(sampleSize)
_ = otv.View(cloud)

# %%
# Draw the limit state surface
# ----------------------------

# %%
bounds = ot.Interval(lowerBound, upperBound)

# %%
graph = drawEvent.drawLimitStateCrossCut(bounds)
graph.add(cloud)
_ = otv.View(graph)

# %%
# Fill the event domain with a color
_ = otv.View(drawEvent.fillEventCrossCut(bounds))

# %%
otv.View.ShowAll()
