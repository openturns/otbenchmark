
from openturns.viewer import View
import openturns as ot
from math import sqrt


# A parametrized class
class CrueFunction(ot.OpenTURNSPythonFunction):
    # H_d : Hauteur de la digue
    # Z_b : Côte de la berge
    # L : Longueur de la rivière
    # B : Largeur de la rivière
    def __init__(self, H_d, Z_b, L, B):
        super(CrueFunction, self).__init__(4, 1)
        self._H_d = H_d
        self._Z_b = Z_b
        self._L = L
        self._B = B
        # Z_d : côte de la digue
        self._Z_d = self._Z_b + self._H_d

    def _exec(self, X):
        Q, K_s, Z_v, Z_m = X
        alpha = (Z_m - Z_v) / self._L
        H = (Q / (K_s * self._B * sqrt(alpha))) ** (3.0 / 5.0)
        Z_c = H + Z_v
        S = Z_c - self._Z_d
        return [S]


H_d = 3.0  # Hauteur de la digue
Z_b = 55.5  # Côte de la berge
L = 5.0e3  # Longueur de la rivière
B = 300.0  # Largeur de la rivière

myParametricWrapper = CrueFunction(H_d, Z_b, L, B)
myWrapper = ot.Function(myParametricWrapper)

# 2. Random vector definition
Q = ot.Gumbel(1.0 / 558.0, 1013.0)
Q = ot.TruncatedDistribution(Q, 0.0, ot.TruncatedDistribution.LOWER)
K_s = ot.Normal(30.0, 7.5)
K_s = ot.TruncatedDistribution(K_s, 0.0, ot.TruncatedDistribution.LOWER)
Z_v = ot.Uniform(49.0, 51.0)
Z_m = ot.Uniform(54.0, 56.0)

# 3. Create the joint distribution function,
#    the output and the event.
inputDistribution = ot.ComposedDistribution([Q, K_s, Z_v, Z_m])
inputRandomVector = ot.RandomVector(inputDistribution)
outputRandomVector = ot.CompositeRandomVector(myWrapper, inputRandomVector)

# 4. Get a sample of the output
sampleS = outputRandomVector.getSample(500)

# 5. Plot the histogram

barsNumber = int(sqrt(sampleS.getSize()))
histoGraph = ot.HistogramFactory().build(sampleS).drawPDF()
histoGraph.setTitle("Histogramme de la surverse")
histoGraph.setXTitle("S (m)")
histoGraph.setYTitle("Frequence")
histoGraph.setLegends([""])
View(histoGraph).show()
