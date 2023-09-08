import numpy as np


# Adding assertions to check for NaN in weights and biases
class MultiLevelPerceptron:
    def __init__(self, layers):
        self.layers = layers
        self.weights = []
        self.biases = []
        self.activation_function = self.linear
        self._initialize_weights_and_biases()

    def linear(self, x):
        return x

    @staticmethod
    def mse(y_true, y_pred):
        return np.mean((y_true - y_pred) ** 2)

    @staticmethod
    def scale_data(x, y):
        global_min = min(0, np.min(y))  # Assuming X is between 0 and 1
        global_max = max(1, np.max(y))
        x_scaled = MultiLevelPerceptron.minmax_scale(X, global_min, global_max)
        y_scaled = MultiLevelPerceptron.minmax_scale(y, global_min, global_max)
        return x_scaled, y_scaled

    @staticmethod
    def minmax_scale(data, min_val, max_val):
        return (data - min_val) / (max_val - min_val)

    def _initialize_weights_and_biases(self):
        self.weights = []
        self.biases = []
        for i in range(len(self.layers) - 1):
            weight_matrix = np.random.randn(self.layers[i + 1], self.layers[i])
            self.weights.append(weight_matrix)
            bias_matrix = np.zeros((self.layers[i + 1], 1))
            self.biases.append(bias_matrix)

    def predict(self, x):

        x = np.array(x).reshape(-1, 1)
        activations = [x]
        zs = []

        for weight, bias in zip(self.weights, self.biases):
            z = np.dot(weight, x) + bias
            zs.append(z)
            x = self.activation_function(z)
            activations.append(x)

        self.assert_nan(x, activations, zs)

        return x, activations, zs

    def calculate_loss(self, y_true, y_pred):
        return self.mse(y_true, y_pred)

    def backward_propagation(self, y_true, y_pred, activations, zs):
        grad_weights = [np.zeros(w.shape) for w in self.weights]
        grad_biases = [np.zeros(b.shape) for b in self.biases]

        delta = (y_pred - y_true)
        grad_biases[-1] = delta
        grad_weights[-1] = np.dot(delta, activations[-2].T)

        for l in range(2, len(self.layers)):
            z = zs[-l]
            delta = np.dot(self.weights[-l + 1].T, delta)
            grad_biases[-l] = delta
            grad_weights[-l] = np.dot(delta, activations[-l - 1].T)

        return grad_weights, grad_biases

    def assert_nan(self, x, activations, zs):
        # Assertions to check for NaN in weights and biases
        for i, w in enumerate(self.weights):
            assert not np.isnan(w).any(), f'NaN found in weights at index {i}'
        for i, b in enumerate(self.biases):
            assert not np.isnan(b).any(), f'NaN found in biases at index {i}'
        for i, b in enumerate(x):
            assert not np.isnan(b).any(), f'NaN found in x at index {i}'
        for i, b in enumerate(activations):
            assert not np.isnan(b).any(), f'NaN found in activations at index {i}'
        for i, b in enumerate(zs):
            assert not np.isnan(b).any(), f'NaN found in zs at index {i}'
    def update_parameters(self, grad_weights, grad_biases, learning_rate):
        self.weights = [w - learning_rate * gw for w, gw in zip(self.weights, grad_weights)]
        self.biases = [b - learning_rate * gb for b, gb in zip(self.biases, grad_biases)]

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            for x_val, y_val in zip(X, y):
                y_pred, activations, zs = self.predict(x_val)
                loss = self.calculate_loss(y_val, y_pred)
                grad_weights, grad_biases = self.backward_propagation(y_val, y_pred, activations, zs)
                self.update_parameters(grad_weights, grad_biases, learning_rate)

            if epoch % 10 == 0:
                print(f"Epoch {epoch}, Loss: {loss}")


# Generate data
def generate_data(num_samples=1000):
    X = np.random.rand(num_samples)
    y = X * 100
    return X, y

X, y = generate_data()

X, y = MultiLevelPerceptron.scale_data(X, y)

# Initialize and train the neural network
mlp = MultiLevelPerceptron([1, 4, 3, 2, 1])

#mlp.train(X, y, epochs=1000, learning_rate=0.01)

# Test the trained network
for i in range(0, 10):
    X_test, y_test = generate_data(num_samples=1)
    print("Generated: ", X_test, " expect:", y_test, " predict:", mlp.predict(X_test)[0])
