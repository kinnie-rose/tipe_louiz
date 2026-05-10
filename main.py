#!/usr/bin/python3

import argparse
import os
import json
import csv
import numpy as np

from generate_config_file import generate_json
from analyze_images import analyze_test_tube

# création d'une liste contenant les chemins vers les images
parser = argparse.ArgumentParser()
parser.add_argument(
    "images_directory_path",
    help="specify the images directory in wich there is a .json file",
)

args = parser.parse_args()
IMAGE_DIRECTORY_PATH = args.images_directory_path
CONFIG_FILE_PATH = os.path.join(IMAGE_DIRECTORY_PATH, "config.json")


images = os.listdir(IMAGE_DIRECTORY_PATH)
if "output.csv" in images:
    raise Exception("there is an output.csv file in the images directory")

images = [os.path.join(IMAGE_DIRECTORY_PATH, i) for i in images if i != "config.json"]

# création du fichier de configuration
if not os.path.isfile(CONFIG_FILE_PATH):
    config = generate_json(CONFIG_FILE_PATH, images[0])
else:
    with open(CONFIG_FILE_PATH, "r") as file:
        config = json.load(file)


# analyse des images
data = np.zeros((len(config["test_tubes"]), len(images)))
for index_tube, tube in enumerate(config["test_tubes"]):
    for index_image, image in enumerate(images):
        data[index_tube, index_image] = analyze_test_tube(
            image,
            config[tube]["tube_borders"],
            config[tube]["x_coordonates"],
            config["scale"],
            config["origin"],
        )


print(data)


# enregistrement des données dans un fichier csv
with open(os.path.join(IMAGE_DIRECTORY_PATH, "output.csv"), "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for index_tube, tube in enumerate(config["test_tubes"]):
        writer.writerow([tube] + list(data[index_tube]))
