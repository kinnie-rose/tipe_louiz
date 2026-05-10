import numpy as np
import cv2


def determine_level_for_an_x(image, x):
    colors = image[:, x]
    min_val = colors.min()
    max_val = colors.max()

    # normalisation entre 0 et 1
    norm = (colors - min_val) / (max_val - min_val)
    gradient = np.diff(norm)

    # variations statistiquement significatives
    seuil_gradient = np.mean(gradient) - 2 * np.std(gradient)
    transitions = np.where(gradient < seuil_gradient)[0]

    return transitions


def analyze_test_tube(image_path, tube_borders, x_coordonates, scale, origin):
    image = cv2.imread(cv2.samples.findFile(image_path), cv2.IMREAD_GRAYSCALE)
    image = image[tube_borders[0][0] : tube_borders[0][1], tube_borders[1][0] : tube_borders[1][1]]

    # amélioration du contraste
    clahe = cv2.createCLAHE(clipLimit=2.0)
    image = clahe.apply(image)

    # flou pour réduire le bruit
    image = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)

    level = []
    for x in x_coordonates:
        level.extend(determine_level_for_an_x(image, x))

    return (origin - (np.mean(level) + tube_borders[0][0])) * scale


if __name__ == "__main__":
    IMAGE_PATH = "IMAGES/Image16.bmp"
    print(analyze_test_tube(IMAGE_PATH, ((320, 430), (150, 300)), (50, 60, 70), 0.065, 442.929))
