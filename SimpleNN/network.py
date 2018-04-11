
class network:
    import math, random
    def __init__(self, neuron_matrix):
        self.layers = [self.layer(n) for n in neuron_matrix]

    def feed_forward(input_vector):
        if len(input_vector) == len(self.layers[0]):
            for layer in layers:
                input_vector = layer.run(input_vector)
            return input_vector[:-1]

    class layer:
        def __init__(self, n):
            self.neurons = [self.neuron(n) for i in range(n)]

        def __len__(self):
            return len(self.neurons)

        def run(self, input):
            return [n.output(input) for n in self.neurons]

        class neuron:
            @staticmethod
            def sigmoid(x):
                return 1 / ( 1 + network.math.e ** -x)

            def __init__(self, input_len):
                self.value = 1
                self.weights = [self.weight() for i in range(input_len)]

            def output(input):
                return neuron.sigmoid(sum(input))

            class weight:

                def __init__(self):
                    self.value = network.random.uniform(-1, 1)

                def next(self, v):
                    self.new = v

                def update(self):
                    self.value = self.new

n = network([5,5,5])
