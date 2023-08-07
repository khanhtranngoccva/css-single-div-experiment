import sys

import cv2
import numpy
from PIL import Image
from scipy.spatial import Delaunay

import chunks_util
import earcut


def find_contours_of_image(image: Image.Image):
    rgb = numpy.array(image.convert('RGB'))
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    polygons = []
    approx_contours = []
    failed = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.001 * cv2.arcLength(contour, True), True)
        squeezed = approx.squeeze()

        if len(squeezed) > 2:
            polygon = []
            for x, y in squeezed:
                polygon.append(x)
                polygon.append(y)
            triangulation = earcut.earcut(polygon)

            if len(triangulation) == 0 and len(approx) >= 3:
                print("Triangulation failure - a polygon failed to be converted into triangles", len(triangulation),
                      len(approx), file=sys.stderr)
                failed.append(approx)

            for triangle in chunks_util.chunks(triangulation, 3):
                raw_triangle = []
                for vertex in triangle:
                    x, y = squeezed[vertex]
                    raw_triangle.append((x, y))
                polygons.append(raw_triangle)

            approx_contours.append(approx)

    return polygons, approx_contours, failed
