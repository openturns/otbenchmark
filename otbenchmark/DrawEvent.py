# -*- coding: utf-8 -*-
"""
Static methods to plot reliability problems.
"""
import openturns as ot
import pylab as pl
import openturns.viewer as otv


def LinearSample(xmin, xmax, npoints=100):
    """
    Returns a sample created from a regular grid
    from xmin to xmax with npoints points.

    Because of a limitation in OpenTURNS's graphics, we returns
    a ot.Graph when the graphics is 2D and a Matplotlib.figure
    when the plot is a grid of Graphs.
    This limitation may be solved in future releases.

    Parameters
    ----------
    xmin : a float
        The lower bound.
    xmax : a float
        The upper bound.
    npoints : an int
        The number of points.

    Returns
    -------
    sample : a ot.Sample.
        The regular grid with dimension 1 and size npoints.
    """
    step = (xmax - xmin) / (npoints - 1)
    rg = ot.RegularGrid(xmin, step, npoints)
    vertices = rg.getVertices()
    return vertices


class DrawEvent:
    def __init__(
        self,
        event,
        insideEventPointColor="lightsalmon3",
        outsideEventPointColor="darkseagreen3",
        insideEventFillColor="lightsalmon1",
        outsideEventFillColor="darkseagreen1",
    ):
        """
        Create an event with draw services.

        The limit state function must be in dimension > 1 only.

        Parameters
        ----------
        event : an ot.Event
            The event we want to draw.
        insideEventPointColor : a string
            The color of the points inside the event.
            Suggested colors: "forestgreen", "darkolivegreen".
        outsideEventPointColor : a string
            The color of the points outside of the event.
            Suggested colors: "orange", "orangered".
        insideEventFillColor : a string
            The color of the filled domains inside the event.
        outsideEventFillColor : a string
            The color of the filled domains outside of the event.
        """
        #
        g = event.getFunction()
        inputDimension = g.getInputDimension()
        if inputDimension == 1:
            raise ValueError(
                "The input dimension of the function "
                "is equal to 1 but should be > 1."
            )
        self.event = event
        self.insideEventPointColor = insideEventPointColor
        self.outsideEventPointColor = outsideEventPointColor
        self.insideEventFillColor = insideEventFillColor
        self.outsideEventFillColor = outsideEventFillColor
        self.g = event.getFunction()
        self.inputDimension = self.g.getInputDimension()
        return None

    def drawLimitState(self, bounds, nX=50, nY=50):
        """
        Draw the limit state of an event.

        This produces a matrix of cross cuts.

        Parameters
        ----------
        bounds: an ot.Interval
            The lower and upper bounds of the interval.
        nX : an int
            The number of points in the X axis.
        nY : an int
            The number of points in the Y axis.

        Returns
        -------
        fig : matplotlib.figure
            The plot.
        """
        if bounds.getDimension() != self.inputDimension:
            raise ValueError(
                "The input dimension of the bounds "
                "is equal to %d but should be %d."
                % (bounds.getDimension(), self.inputDimension)
            )
        #
        fig = pl.figure(figsize=(12, 12))
        _ = fig.suptitle("Limit state")
        if self.inputDimension == 2:
            graph = self.drawLimitStateCrossCut(bounds, 0, 1, nX, nY)
            _ = otv.View(graph, figure=fig)
        else:
            lowerBound = bounds.getLowerBound()
            upperBound = bounds.getUpperBound()
            for i in range(self.inputDimension):
                for j in range(i + 1, self.inputDimension):
                    crossCutLowerBound = [lowerBound[i], lowerBound[j]]
                    crossCutUpperBound = [upperBound[i], upperBound[j]]
                    crossCutBounds = ot.Interval(crossCutLowerBound, crossCutUpperBound)
                    graph = self.drawLimitStateCrossCut(crossCutBounds, i, j, nY)
                    index = i * (self.inputDimension - 1) + j
                    ax = fig.add_subplot(
                        self.inputDimension - 1, self.inputDimension - 1, index
                    )
                    _ = otv.View(graph, figure=fig, axes=[ax])
        return fig

    def drawLimitStateCrossCut(self, bounds, i=0, j=1, nX=50, nY=50):
        """
        Draw the cross-cut of the limit state of an event on a cross-cut.

        Parameters
        ----------
        bounds: an ot.Interval
            The lower and upper bounds of the cross-cut interval.
        i : int
            The index of the first marginal of the cross-cut.
        j : int
            The index of the second marginal of the cross-cut.
        nX : an int
            The number of points in the X axis.
        nY : an int
            The number of points in the Y axis.

        Returns
        -------
        graph : ot.Graph
            The plot of the (i, j) cross cut.
        """
        if bounds.getDimension() != 2:
            raise ValueError(
                "The input dimension of the bounds "
                "is equal to %d but should be 2." % (bounds.getDimension())
            )
        #
        threshold = self.event.getThreshold()
        description = self.g.getInputDescription()
        boxExperiment = ot.Box([nX, nY], bounds)
        reducedInputSample = boxExperiment.generate()
        crosscutFunction = self.buildCrossCutFunction(i, j)
        outputSample = crosscutFunction(reducedInputSample)
        #
        graph = ot.Graph(
            "Limit state surface", description[i], description[j], True, ""
        )
        # Create the contour
        levels = ot.Point([threshold])
        labels = [str(threshold)]
        drawLabels = True
        lowerBound = bounds.getLowerBound()
        upperBound = bounds.getUpperBound()
        x = LinearSample(lowerBound[0], upperBound[0], nX + 2)
        y = LinearSample(lowerBound[1], upperBound[1], nY + 2)
        contour = ot.Contour(x, y, outputSample, levels, labels, drawLabels)
        graph.add(contour)
        return graph

    def drawSample(self, sampleSize):
        """
        Draw the sample of an event.

        The points inside and outside the event are colored.

        Parameters
        ----------
        sampleSize: int
            The sample size.

        Returns
        -------
        fig : Matplotlib.figure
            The plot.
        """
        fig = pl.figure(figsize=(12, 12))
        _ = fig.suptitle("Limit state")
        if self.inputDimension == 2:
            graph = self.drawSampleCrossCut(sampleSize, 0, 1)
            _ = otv.View(graph, figure=fig)
        else:
            for i in range(self.inputDimension):
                for j in range(i + 1, self.inputDimension):
                    graph = self.drawSampleCrossCut(sampleSize, i, j)
                    index = i * (self.inputDimension - 1) + j
                    ax = fig.add_subplot(
                        self.inputDimension - 1, self.inputDimension - 1, index
                    )
                    _ = otv.View(graph, figure=fig, axes=[ax])
        return fig

    def drawSampleCrossCut(self, sampleSize, i=0, j=1):
        """
        Draw the sample of an event on a cross-cut.

        The points inside and outside the event are colored.

        The algorithm uses the getMarginal() method
        of the distribution in order to create the bivariate distribution.
        Then the sample is generated from this bivariate distribution.
        A more rigorous method would draw the conditional distribution,
        but this might reduce the performance in general.
        https://github.com/mbaudin47/otbenchmark/issues/47

        Parameters
        ----------
        sampleSize: int
            The sample size.
        i : int
            The index of the first marginal of the cross-cut.
        j : int
            The index of the second marginal of the cross-cut.

        Returns
        -------
        graph : ot.Graph
            The plot.
        """
        inputVector = self.event.getAntecedent()
        distribution = inputVector.getDistribution()
        marginalDistribution = distribution.getMarginal([i, j])
        inputSample = marginalDistribution.getSample(sampleSize)
        crosscutFunction = self.buildCrossCutFunction(i, j)
        outputSample = crosscutFunction(inputSample)
        threshold = self.event.getThreshold()
        operator = self.event.getOperator()
        #
        sampleSize = outputSample.getSize()
        insideIndices = []
        outsideIndices = []
        for k in range(sampleSize):
            y = outputSample[k, 0]
            isInside = operator(y, threshold)
            if isInside:
                insideIndices.append(k)
            else:
                outsideIndices.append(k)
        #
        insideSample = ot.Sample([inputSample[k] for k in insideIndices])
        outsideSample = ot.Sample([inputSample[k] for k in outsideIndices])
        #
        description = self.g.getInputDescription()
        title = "Points X s.t. g(X) %s %s" % (operator, threshold)
        graph = ot.Graph(title, description[i], description[j], True, "")
        if len(insideIndices) > 0:
            cloud = ot.Cloud(insideSample, self.insideEventPointColor, "fsquare", "In")
            graph.add(cloud)
        if len(outsideIndices) > 0:
            cloud = ot.Cloud(
                outsideSample, self.outsideEventPointColor, "fsquare", "Out"
            )
            graph.add(cloud)
        graph.setLegendPosition("topright")
        return graph

    def drawInputOutputSample(self, inputSample, outputSample):
        """
        Draw the sample of an event.
        The points inside and outside the event are colored.

        Parameters
        ----------
        inputSample: an ot.Sample
            The input 2D sample.
        outputSample: an ot.Sample
            The output 1D sample.
        Returns
        -------
        None.
        """
        if inputSample.getDimension() != 2:
            raise ValueError(
                "The input dimension of the input sample "
                "is equal to %d but should be 2." % (inputSample.getDimension())
            )
        #
        threshold = self.event.getThreshold()
        g = self.event.getFunction()
        operator = self.event.getOperator()
        #
        sampleSize = outputSample.getSize()
        insideIndices = []
        outsideIndices = []
        for i in range(sampleSize):
            y = outputSample[i, 0]
            isInside = operator(y, threshold)
            if isInside:
                insideIndices.append(i)
            else:
                outsideIndices.append(i)
        #
        insideSample = ot.Sample([inputSample[i] for i in insideIndices])
        outsideSample = ot.Sample([inputSample[i] for i in outsideIndices])
        #
        description = g.getInputDescription()
        title = "Points X s.t. g(X) %s %s" % (operator, threshold)
        graph = ot.Graph(title, description[0], description[1], True, "")
        if len(insideIndices) > 0:
            cloud = ot.Cloud(insideSample, self.insideEventPointColor, "fsquare", "In")
            graph.add(cloud)
        if len(outsideIndices) > 0:
            cloud = ot.Cloud(
                outsideSample, self.outsideEventPointColor, "fsquare", "Out"
            )
            graph.add(cloud)
        graph.setLegendPosition("topright")
        return graph

    def fillEvent(self, bounds, nX=50, nY=50):
        """
        Draw the sample of an event.

        The points inside and outside the event are colored.

        Parameters
        ----------
        sampleSize: int
            The sample size.

        Returns
        -------
        fig : Matplotlib.figure
            The plot.
        """
        if bounds.getDimension() != self.inputDimension:
            raise ValueError(
                "The input dimension of the bounds "
                "is equal to %d but should be %d."
                % (bounds.getDimension(), self.inputDimension)
            )
        fig = pl.figure(figsize=(12, 12))
        _ = fig.suptitle("Limit state")
        if self.inputDimension == 2:
            graph = self.fillEventCrossCut(bounds, 0, 1, nX, nY)
            _ = otv.View(graph, figure=fig)
        else:
            lowerBound = bounds.getLowerBound()
            upperBound = bounds.getUpperBound()
            for i in range(self.inputDimension):
                for j in range(i + 1, self.inputDimension):
                    crossCutLowerBound = [lowerBound[i], lowerBound[j]]
                    crossCutUpperBound = [upperBound[i], upperBound[j]]
                    crossCutBounds = ot.Interval(crossCutLowerBound, crossCutUpperBound)
                    graph = self.fillEventCrossCut(crossCutBounds, i, j, nX, nY)
                    index = i * (self.inputDimension - 1) + j
                    ax = fig.add_subplot(
                        self.inputDimension - 1, self.inputDimension - 1, index
                    )
                    _ = otv.View(graph, figure=fig, axes=[ax])
        return fig

    def fillEventCrossCut(self, bounds, i=0, j=1, nX=50, nY=50):
        """
        Fill the space inside an event with a color on a cross-cut.

        Parameters
        ----------
        bounds: an ot.Interval
            The lower and upper bounds of the cross-cut interval.
        i : int
            The index of the first marginal of the cross-cut.
        j : int
            The index of the second marginal of the cross-cut.
        nX : int
            The number of points in the X axis.
        nY : int
            The number of points in the Y axis.

        Returns
        -------
        graph : ot.Graph
            The plot.
        """
        if bounds.getDimension() != 2:
            raise ValueError(
                "The input dimension of the bounds "
                "is equal to %d but should be 2." % (bounds.getDimension())
            )
        #
        threshold = self.event.getThreshold()
        operator = self.event.getOperator()
        # Define the number of intervals in each direction of the box
        myIndices = [nX, nY]
        myMesher = ot.IntervalMesher(myIndices)
        mesh = myMesher.build(bounds)
        #
        simplices = mesh.getSimplices()
        vertices = mesh.getVertices()
        numberOfSimplices = mesh.getSimplicesNumber()
        #
        crosscutFunction = self.buildCrossCutFunction(i, j)
        polyDataInside = []
        polyDataOutside = []
        for i in range(numberOfSimplices):
            simplex = simplices[i]
            corners = [
                vertices[simplex[0]],
                vertices[simplex[1]],
                vertices[simplex[2]],
                vertices[simplex[2]],
            ]
            sampleInput = ot.Sample(corners)
            sampleOutput = crosscutFunction(sampleInput)
            mean = sampleOutput.computeMean()[0]
            if operator(mean, threshold):
                polyDataInside.append(corners)
            else:
                polyDataOutside.append(corners)

        # Create PolygonArray from list of polygons inside event
        def CreatePolygonArray(polyData, color):
            numberOfPolygons = len(polyData)
            polygonList = [
                ot.Polygon(polyData[i], color, color) for i in range(numberOfPolygons)
            ]
            polygonArray = ot.PolygonArray(polygonList)
            return polygonArray

        polygonArrayInside = CreatePolygonArray(
            polyDataInside, self.insideEventFillColor
        )
        polygonArrayOutside = CreatePolygonArray(
            polyDataOutside, self.outsideEventFillColor
        )
        #
        description = self.g.getInputDescription()
        title = "Domain where g(x) %s %s" % (operator, threshold)
        graph = ot.Graph(title, description[0], description[1], True, "topright")
        graph.add(polygonArrayInside)
        graph.add(polygonArrayOutside)
        graph.setLegends(["In", "Out"])
        return graph

    def buildCrossCutFunction(self, i, j):
        """
        Create the cross-cut parametric function for projection (i,j).

        The parametric function is the event function where the
        only free variables are (X[i], X[j]) and other variables
        are set to the mean point.

        We must have i < j, otherwise the function
        would be evaluated at the wrong input X.

        Parameters
        ----------
        i : int
            The index of the first marginal of the cross-cut.
        j : int
            The index of the second marginal of the cross-cut.

        Returns
        -------
        crosscutFunction : ot.Function
            The cross-cut function.
        """
        if j < i:
            raise ValueError("i=%d > j=%d." % (i, j))
        inputVector = self.event.getAntecedent()
        distribution = inputVector.getDistribution()
        mean = distribution.getMean()
        indices = []
        point = []
        for k in range(self.inputDimension):
            if k != i and k != j:
                indices.append(k)
                point.append(mean[k])
        crosscutFunction = ot.ParametricFunction(self.g, indices, point)
        return crosscutFunction

    def draw(
        self,
        bounds,
        sampleSize=1000,
        nX=50,
        nY=50,
        drawLimitState=True,
        drawSample=True,
        fillEvent=False,
    ):
        """
        Draw the event, superimposing the graphics.

        Parameters
        ----------
        sampleSize: int
            The sample size.
        bounds: an ot.Interval
            The lower and upper bounds of the cross-cut interval.
        nX : int
            The number of points in the X axis.
        nY : int
            The number of points in the Y axis.
        drawLimitState : bool
            If True, draw the limit state surface.
        drawSample : bool
            If True, draw the sample.
        fillEvent : bool
            If True, fill the event.

        Returns
        -------
        fig : Matplotlib.figure
            The plot.
        """
        if not drawLimitState and not drawSample and not fillEvent:
            raise ValueError("At least one boolean flag must be True.")
        if bounds.getDimension() != self.inputDimension:
            raise ValueError(
                "The input dimension of the bounds "
                "is equal to %d but should be %d."
                % (bounds.getDimension(), self.inputDimension)
            )
        fig = pl.figure(figsize=(12, 12))
        _ = fig.suptitle("Limit state")
        if self.inputDimension == 2:
            graph = self.fillEventCrossCut(bounds, 0, 1, nX, nY)
            _ = otv.View(graph, figure=fig)
        else:
            lowerBound = bounds.getLowerBound()
            upperBound = bounds.getUpperBound()
            inputDescription = self.g.getInputDescription()
            for i in range(self.inputDimension):
                for j in range(i + 1, self.inputDimension):
                    crossCutLowerBound = [lowerBound[i], lowerBound[j]]
                    crossCutUpperBound = [upperBound[i], upperBound[j]]
                    crossCutBounds = ot.Interval(crossCutLowerBound, crossCutUpperBound)
                    graph = ot.Graph("", "", "", True)
                    graph.setXTitle(inputDescription[i])
                    graph.setYTitle(inputDescription[j])
                    if fillEvent:
                        plot = self.fillEventCrossCut(crossCutBounds, i, j, nX, nY)
                        graph.add(plot)
                    if drawLimitState:
                        plot = self.drawLimitStateCrossCut(crossCutBounds, i, j, nY)
                        graph.add(plot)
                    if drawSample:
                        plot = self.drawSampleCrossCut(sampleSize, i, j)
                        graph.add(plot)
                    index = i * (self.inputDimension - 1) + j
                    ax = fig.add_subplot(
                        self.inputDimension - 1, self.inputDimension - 1, index
                    )
                    _ = otv.View(graph, figure=fig, axes=[ax])
        return fig
