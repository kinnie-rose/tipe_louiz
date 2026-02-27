import json
import matplotlib.pyplot as plt
import cv2


def generate_json(config_file_path, image):
    IMAGE = cv2.imread(cv2.samples.findFile(image), cv2.IMREAD_GRAYSCALE)

    nb_tubes = int(input("combien de tubes : "))
    questions = ["equerre à 0 cm", "equerre à 5 cm"] + [
        "haut gauche du tube",
        "bas droite du tube",
    ] * nb_tubes

    values = []
    i = 0

    fig, ax = plt.subplots()
    ax.imshow(IMAGE, cmap="gray")

    def onclick(event):
        nonlocal i, values
        if event.xdata is not None and event.ydata is not None:
            i += 1
            values.append([event.xdata, event.ydata])
            if i < len(questions):
                print(questions[i])
            else:
                plt.close()

    cid = fig.canvas.mpl_connect("button_press_event", onclick)

    print(questions[0])

    plt.show()

    data = {}

    # calcul de l'échelle en cm/pixel
    data["scale"] = 5 / (values[0][1] - values[1][1])

    # données sur les tubes
    values = values[2:]
    data["test_tubes"] = ["tb" + str(i + 1) for i in range(len(values) // 2)]

    i = 0
    for nom_tube in data["test_tubes"]:
        data[nom_tube] = {}
        data[nom_tube]["tube_borders"] = [
            [int(values[i][1]), int(values[i + 1][1])],
            [int(values[i][0]), int(values[i + 1][0])],
        ]

        tube_borders = data[nom_tube]["tube_borders"]
        x_coordonates = []

        img = IMAGE[
            tube_borders[0][0] : tube_borders[0][1], tube_borders[1][0] : tube_borders[1][1]
        ]

        fig, ax = plt.subplots()
        ax.imshow(img)

        def onclick_2(event):
            if event.xdata is not None and event.ydata is not None:
                x_coordonates.append(int(event.xdata))

        cid = fig.canvas.mpl_connect("button_press_event", onclick_2)

        print(f"cliquer sur les coordonnées x où chercher le niveau pour {nom_tube}")

        plt.show()

        data[nom_tube]["x_coordonates"] = x_coordonates

        i += 2

    with open(config_file_path, "w") as file:
        json.dump(data, file)

    return data
