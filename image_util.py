from PIL import Image


def get_image_rgb_matrix(image: Image.Image):
    width = image.width
    height = image.height
    data = list(image.convert("RGB").getdata())
    matrix = [[data[y * width + x] for x in range(width)] for y in range(height)]
    return matrix
