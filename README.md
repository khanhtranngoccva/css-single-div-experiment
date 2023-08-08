# CSS Single Div Experiment in Python with BFS and OpenCV
![image](https://github.com/khanhtranngoccva/css-single-div-experiment/assets/61155608/ba086a26-815c-4b82-9a96-d140bf5a173d)

## Original clip-path implementation
The clip-path implementation from Junferno @kevinjycui is obviously infinitely more robust and compact than this method, as clip-path already assists with shape drawing out of the box. 
<a href="https://github.com/kevinjycui/css-video">ORIGINAL IMPLEMENTATION</a>

However, unlike Junferno's original implementation, this experiment aims to achieve the transformation of images into pure, no-div CSS - no extra HTML but the link to the original stylesheet is allowed.

## Abstract steps
1. Use breadth-first search in order to spot contiguous regions with the same color.
2. Use pre-provided OpenCV edge detection algorithms to draw approximate polygons around the image.
![image](https://github.com/khanhtranngoccva/css-single-div-experiment/assets/61155608/28e604f2-6fb2-4697-b459-f9ee4e98d397)
3. Use the earcut library to triangulate the image. Each triangle will have a color attached to it based on the color of the previous region.
![image](https://github.com/khanhtranngoccva/css-single-div-experiment/assets/61155608/11eeb57a-e6af-4a48-9009-87d1504205d0)
4. For each triangle, split it into 2 halves with a horizontal cut. This creates 2 triangles, both of which have exactly 2 points having the same y-coordinate, which is necessary for conic-gradients to work.
5. Convert mini-triangles created from step 4 into conic gradients.

## Optimizations
1. Only handle 1 region at a time and the contiguous region BFS detector is an iterator instead of a normal function. This is necessary in order to prevent heavy RAM consumption, crashing the script.
2. Added extra angle parameters to minimize gaps between triangles due to browser rounding errors.

## Limitations
1. Concave polygons and polygons with holes don't always triangulate properly. Sometimes they are omitted by the script, unfortunately, these polygons ended up hidden from the screen. (example: area enclosed by red lines indicate a failure to triangulate)
![image](https://github.com/khanhtranngoccva/css-single-div-experiment/assets/61155608/0f6ce527-f372-4822-b5ee-ded440f59a60)
2. Triangulation of polygons is incredibly space-intensive. A simple image as in the demo can take up thousands of triangles, corresponding to megabytes of data. More complex images can take up
hundreds of thousands of triangles (conic gradients) which then crash the browser.

## Possible alternative solution(s) to limitation(s)
Alternative 1: 
* Forfeit minor details and rely on converting the entire image into a low-poly Delaunay triangular mesh. Each triangle will then take the color of its centroid.
* Convert each triangle into 2 conic-gradients as done in this repo.
