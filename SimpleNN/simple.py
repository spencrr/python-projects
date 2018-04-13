    class network:
        import numpy as np
        import matplotlib.pyplot as plt

        class neuron:
            def __init__(self, is_input, is_bias, input_len):
                self.value = 1
                self.is_input = is_input
                self.is_bias = is_bias
                self.weights = network.np.ndarray(shape=(input_len))

            def feed(self, input_vector):
                if not self.is_bias:
                    if not self.is_input:
                        self.value = network.non_lin(network.np.dot(input_vector, self.weights))
                    else:
                        self.value = input_vector
                return self.value

        @staticmethod
        def non_lin(z, deriv=False):
            if deriv:
                s = network.non_lin(z)
                return  s * (1 - s)
            return 1 / (1 + network.np.exp(-z))

        @staticmethod
        def cost_func(a, b):
            return network.np.sum((a - b) ** 2)


        def __init__(self, neuron_vector):
            # self.neurons = [[network.neuron(i == 0, n == neuron_vector[i], neuron_vector[i - 1] + 1 if i  > 0 else 0)
            #         for n in range(neuron_vector[i] + (1 if i < len(neuron_vector) - 1 else 0))
            #         ] for i in range(len(neuron_vector))]
            input = [[network.neuron(True, i == neuron_vector[0], neuron_vector[0]) for i in range(neuron_vector[0] + 1)]]
            hidden_output = [[network.neuron(False, n == neuron_vector[i], neuron_vector[i-1] + 1) for n in range(neuron_vector[i] + 1)] for i in range(1, len(neuron_vector))]
            self.neurons = input + hidden_output
            for layer in self.neurons:
                print(len(layer))
                for n in layer:
                    print('{} {} {}'.format(n.is_input, n.is_bias, len(n.weights)))

        def forward(self, input_vector):
            if len(self.neurons[0]) - 1 == len(input_vector):
                for layer in range(len(self.neurons)):
                    output_vector = []
                    for neuron in range(len(self.neurons[layer]) + 1):
                        print(layer, neuron)
                        output_vector.append(
                        self.neurons[layer][neuron].feed(input_vector[neuron] if layer == 0 else input_vector))
                    input_vector = output_vector
                return input_vector
        def test(self):
            # X = network.np.linspace(-5, 5, 50)
            # y = network.non_lin(X)
            # y_prime = network.non_lin(X, deriv=True)
            # network.plt.scatter(X, y)
            # network.plt.show()
            pass



    n = network([3, 8, 3, 3])
    n.test()
    n.forward([1,2,3])
