import numpy as np
import matplotlib.pyplot as plt
import cv2


IMAGE_PATH = "/media/kinnie-rose/Data/code/python/tipe_lmleq/Image16.bmp"


def find_transition(image_path, borders, x):
    image = cv2.imread(cv2.samples.findFile(image_path), cv2.IMREAD_GRAYSCALE)
    # x = 1024, y =768

    image = image[borders[0][0] : borders[0][1], borders[1][0] : borders[1][1]]
    # image = exposure.adjust_gamma(image, 2)

    # Amélioration du contraste
    clahe = cv2.createCLAHE(clipLimit=2.0)
    image = clahe.apply(image)

    # Flou pour réduire le bruit
    image = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)

    colors = image[:, x]
    min_val = colors.min()
    max_val = colors.max()

    # normalisation entre 0 et 1
    norm = (colors - min_val) / (max_val - min_val)

    gradient = np.diff(norm)
    # gradient = gradient[gradient < 0] # à voir si nécessaire

    seuil_gradient = np.mean(gradient) - 2 * np.std(gradient)  # cf explications

    transitions = np.where(gradient < seuil_gradient)[0]

    # virer les valeurs trop éloignées... est ce qu'on le laisse ?? à tester
    """ mean = np.mean(transitions)
    transitions = list(filter(lambda x: abs(x - mean) < 0.2 * shape_y, transitions))
    """

    print(transitions)
    print(np.mean(transitions))
    plt.imshow(image, cmap="gray")
    plt.show()


if __name__ == "__main__":
    find_transition(IMAGE_PATH, ((320, 430), (150, 300)), 60)
