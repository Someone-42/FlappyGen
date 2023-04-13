from copy import deepcopy # <- Might create some issues
import NeuralNetwork as NN

PERCENTAGE_NEW=0.2

def generate_new_brains(birds, score_last_gen):
    chance = 0.5
    if score_last_gen > 10:
        chance = 0.1
    elif score_last_gen > 3:
        chance = 0.2

    if len(birds) == 0:
        return
        
    birds = sorted(birds, key=lambda bird: bird.score)
    best_bird = birds[-1]
    new_brains = []

    nb_new=int(len(birds)*PERCENTAGE_NEW)
    nb_from_ancestores=len(birds)-nb_new

    for _ in range(nb_new):
        new_brains.append(NN.NeuralNetwork(4, 1))

    for _ in range(nb_from_ancestores):
        new_brain = deepcopy(best_bird.brain) # TODO: Fix performance hit
        new_brain.mutate(NN.mutate(chance))
        new_brains.append(new_brain)
    return new_brains
