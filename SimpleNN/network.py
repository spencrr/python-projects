class network:
    import numpy as np

    @staticmethod
    def relu(z, d=False):
        if d:
            n = network.relu(z)
            return n * (1 - n)
        return 1 / (1 + np.exp(-z))

    @staticmethod
    def cost(a, b, d=False):
        if d:
            return a - b
        return 0.5 * network.np.sum((a - b) ** 2)

    def __init__(self, input, v, output):
        # np.random.seed(1)
        v.append(output)
        self.syn = []
        for l in range(len(v)):
            self.syn.append(network.np.ndarray(shape=(v[l], input), buffer=np.random.uniform(-1, 1, v[l] * (input + 1))))
            input = v[l]
        self.syn = np.array(self.syn)

    def feed(self, input_vector):
        self.output_matrix = []
        for l in self.syn:
            print(input_vector, l.T)
            input_vector = network.relu(np.dot(input_vector, l.T))
            self.output_matrix.append(input_vector)
        return input_vector


def main():
    n = network(100, [100, 100, 100, 100, 100], 100)
    import numpy as np
    n.feed(np.random.uniform(-1, 1, 100))

if __name__ == '__main__':
    main()
