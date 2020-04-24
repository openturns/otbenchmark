# -*- coding: utf-8 -*-
"""
Static methods to plot reliability problems.
"""
import openturns as ot


def LinearSample(xmin, xmax, npoints=100):
    """
    Returns a sample created from a regular grid
    from xmin to xmax with npoints points.

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

        The limit state function must be in dimension 2 only.

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

        Returns
        -------
        self:
            a DrawEvent object
        """
        self.event = event
        #
        g = self.event.getFunction()
        inputDimension = g.getInputDimension()
        if inputDimension != 2:
            raise ValueError(
                "The input dimension of the function "
                "is equal to %d but should be 2." % (inputDimension)
            )
        self.insideEventPointColor = insideEventPointColor
        self.outsideEventPointColor = outsideEventPointColor
        self.insideEventFillColor = insideEventFillColor
        self.outsideEventFillColor = outsideEventFillColor
        return None

    def drawLimitState(self, bounds, nX=50, nY=50):
        """
        Draw the limit state of an event.

        Parameters
        ----------
        event : an ot.Event
            The event we want to draw.

        bounds: an ot.Interval
            The lower and upper bounds of the interval.

        nX : an int
            The number of points in the X axis.

        nY : an int
            The number of points in the Y axis.

        Returns
        -------
        None.

        """
        if bounds.getDimension() != 2:
            raise ValueError(
                "The input dimension of the bounds "
                "is equal to %d but should be 2." % (bounds.getDimension())
            )
        #
        threshold = self.event.getThreshold()
        g = self.event.getFunction()
        #
        boxExperiment = ot.Box([nX, nY], bounds)
        inputSample = boxExperiment.generate()
        outputSample = g(inputSample)
        #
        description = g.getInputDescription()
        graph = ot.Graph(
            "Limit state surface", description[0], description[1], True, ""
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

    def drawSample(self, inputSample, outputSample):
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
        Fill the space inside an event with a color.

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
        None.

        """
        if bounds.getDimension() != 2:
            raise ValueError(
                "The input dimension of the bounds "
                "is equal to %d but should be 2." % (bounds.getDimension())
            )
        #
        threshold = self.event.getThreshold()
        g = self.event.getFunction()
        operator = self.event.getOperator()
        #
        # Define the number of interval in each direction of the box
        myIndices = [nX, nY]
        myMesher = ot.IntervalMesher(myIndices)
        mesh = myMesher.build(bounds)
        #
        simplices = mesh.getSimplices()
        vertices = mesh.getVertices()
        numberOfSimplices = mesh.getSimplicesNumber()
        #
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
            sampleOutput = g(sampleInput)
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
        description = g.getInputDescription()
        title = "Domain where g(x) %s %s" % (operator, threshold)
        graph = ot.Graph(title, description[0], description[1], True, "topright")
        graph.add(polygonArrayInside)
        graph.add(polygonArrayOutside)
        graph.setLegends(["In", "Out"])
        return graph
