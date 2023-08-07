# Credit: @junferno
import PIL.Image
import cv2
import numpy
from PIL import Image
from tqdm import tqdm

import image_util
import bfs_util
import cv_util
import triangle_util

if __name__ == '__main__':
    im = Image.open("test5.png")
    # im = im.resize((im.width * 2, im.height * 2), PIL.Image.BILINEAR)
    matrix = image_util.get_image_rgb_matrix(im)

    region_iterator = bfs_util.bfs_image_matrix(matrix)

    all_triangles = []
    all_contours = []
    failed_contours = []
    for area, color in region_iterator:
        triangles_out, approx_contours, failed = cv_util.find_contours_of_image(Image.fromarray(area))
        for out in triangles_out:
            all_triangles.append([out, color])
        for out in approx_contours:
            all_contours.append([out, color])
        for out in failed:
            failed_contours.append([out, color])

    drawn_triangles = []
    for triangle, color in all_triangles:
        poly = numpy.array(triangle).reshape((-1, 1, 2))
        drawn_triangles.append(poly)

    drawn_contours = []
    for contour, color in all_contours:
        drawn_contours.append(contour)

    drawn_failed_contours = []
    for contour, color in all_contours:
        drawn_failed_contours.append(contour)

    debug_numpy = numpy.array(im.convert("RGB"))
    test_contours = cv2.drawContours(debug_numpy, drawn_contours, -1, (0, 255, 255), 1)
    cv2.imshow("Test contours", test_contours)
    test_triangles = cv2.drawContours(debug_numpy, drawn_triangles, -1, (0, 255, 255), 1)
    cv2.imshow("Test triangles", test_triangles)
    test_failed = cv2.drawContours(debug_numpy, drawn_contours, -1, (0, 0, 255), 1)
    cv2.imshow("Failures", test_failed)

    layers = []
    for triangle, color in all_triangles:
        converted = triangle_util.convert_triangle(triangle, color)
        for layer in converted:
            layers.append(layer)
    layers.reverse()
    layer_string = ',\n'.join(layers)
    rule = """
    html, body {{
        width: 100%;
        height: 100%;
        margin: 0;
    }}
    
    body {{
        background: {};
        background-repeat: no-repeat;
    }}""".format(layer_string)

    with open("styles.css", "w") as f:
        f.write(rule)

    cv2.waitKey(0)
    im.close()
