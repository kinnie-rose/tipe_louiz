#!/usr/bin/python3

import argparse
import os
import json
import csv
import numpy as np

from analyze_images import analyze_test_tube


parser = argparse.ArgumentParser()
parser.add_argument(
    "images_directory_path",
    help="specify the images directory in wich there is a .json file",
)

args = parser.parse_args()
IMAGE_DIRECTORY_PATH = args.images_directory_path


images = os.listdir(IMAGE_DIRECTORY_PATH)
if not "config.json" in images:
    raise Exception("missing a .json file in images directory")
images.remove("config.json")
images = [os.path.join(IMAGE_DIRECTORY_PATH, i) for i in images]
frames_nb = len(images)


with open(os.path.join(IMAGE_DIRECTORY_PATH, "config.json"), "r") as file:
    config = json.load(file)


data = np.zeros((len(config["test_tubes"]), frames_nb))
for index_tube, tube in enumerate(config["test_tubes"]):
    tube_levels = np.zeros(frames_nb)
    for index_image, image in enumerate(images):
        tube_levels[index_image] = analyze_test_tube(
            image, config[tube]["tube_borders"], config[tube]["x_coordonates"]
        )
    data[index_tube] = tube_levels.copy()


print(data)


with open(os.path.join(IMAGE_DIRECTORY_PATH, "output.csv"), "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for index_tube, tube in enumerate(config["test_tubes"]):
        writer.writerow([tube] + list(data[index_tube]))
