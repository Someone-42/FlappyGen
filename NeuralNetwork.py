from Matrix import Matrix
import math
import random


def sigmoid(x):
    return 1/(1+math.e**(-x))


def step(x):
    if x < 0:
        return 0
    else:
        return 1

def toRange(a, b, c, d, e):
    return ((a - b) / (c - b)) * (e - d) + d

def mutate(chance=0.2):
    def mutate_fn(x):
        if random.random()<chance:
            # return x + random.gauss(0, 1)
            return x + random.uniform(-1, 1)
        else:
            return x
    return mutate_fn


class NeuralNetwork:
    __slots__ = ("nb_inputs", "nb_outputs", "poids_input_output",
                 "biais_output", "activation_fn")

    def __init__(self, nb_inputs, nb_outputs):
        self.nb_inputs = nb_inputs
        self.nb_outputs = nb_outputs
        self.poids_input_output = Matrix.random(nb_outputs, nb_inputs)
        self.biais_output = Matrix.random(nb_outputs, 1)
        self.activation_fn = step

    @staticmethod
    def fromDict(dict):
        nn = NeuralNetwork(4, 1)
        nn.poids_input_output = Matrix.from_array(dict["poids"])
        nn.biais_output = Matrix.from_array(dict["biais"])
        return nn

    def predict(self, inputs):
        """
        inputs: Matrix nb_input rows 1 col
        """
        assert inputs.cols == 1 and inputs.rows == self.nb_inputs

        somme_poids = self.poids_input_output * inputs
        res = somme_poids + self.biais_output
        res.mapImpl(lambda i, j, el: self.activation_fn(el))

        return res

    def mutate(self, fn):
        self.poids_input_output.mapImpl(lambda i, j, el: fn(el))
        self.biais_output.mapImpl(lambda i, j, el: fn(el))

    def toDict(self):
        return {
            "biais": self.biais_output.toDict(),
            "poids": self.poids_input_output.toDict()
        }


if __name__ == "__main__":
    nn = NeuralNetwork(4, 1)
    print(nn.poids_input_output)
    print(nn.biais_output)
