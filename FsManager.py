import json
from datetime import datetime
import os
from NeuralNetwork import NeuralNetwork

BASE_PATH = "./saved-brains/"
if not os.path.isdir(BASE_PATH):
    os.mkdir(BASE_PATH)

def save_birds(birds, gen_number):
    birds = list(map(
        lambda b: b.brain.toDict(), birds
    ))

    date_note = datetime.now()
    # Heures-Minutes-Secondes-Jours-Mois-Années
    file_name = date_note.strftime("%H-%M-%S-%d-%m-%y") + ".json"

    content = {
        "generation_number": gen_number,
        "brains": birds
    }

    content = json.dumps(content)

    with open(BASE_PATH + file_name, "w") as f:
        f.write(content)


def load_birds(file_name):
    load_me_path = BASE_PATH + file_name
    if os.path.exists(load_me_path):
        with open(load_me_path, "r") as f:
            content = f.read()
            content = json.loads(content)

            content["brains"] = list(
                map(lambda b: NeuralNetwork.fromDict(b), content["brains"]))

            return content
    return None

def get_save_files():
    """ Retourne une liste de noms des fichiers de sauvegarde """
    return [file for file in os.listdir(BASE_PATH) if file.endswith(".json")]
