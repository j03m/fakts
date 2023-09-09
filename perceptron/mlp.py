import numpy as np
import argparse

_assert_nan = False

# Adding assertions to check for NaN in weights and biases
class MultiLevelPerceptron:
    def __init__(self, layers):
        self.layers = layers
        self.weights = []
        self.biases = []
        self.activation_function = self.linear
        self.activation_derivative = self.linear_derivative
        self._initialize_weights_and_biases()

    def linear(self, x):
        return x

    def linear_derivative(self, z):
        return 1

    def relu(self, x):
        return np.maximum(0, x)

    def relu_derivative(self, z):
        return (z > 0).astype(float)

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
            # weight_matrix = np.random.randn(self.layers[i + 1], self.layers[i])
            weight_matrix = np.random.randn(self.layers[i + 1], self.layers[i]) * np.sqrt(2. / self.layers[i])
            self.weights.append(weight_matrix)
            bias_matrix = np.zeros((self.layers[i + 1], 1))
            self.biases.append(bias_matrix)

    def predict(self, input_):
        x = np.array(input_)

        # Check if x is a scalar
        if x.shape == ():
            x = x.reshape(1, 1)
        elif len(x.shape) == 2:  # If the input is a 2D array
            if x.shape[0] == 1:  # If there's only one sample
                x = x.T  # Transpose to make it a column vector
        else:  # 1D array
            x = x.reshape(-1, 1)  # Reshape to a column vector

        activations = [x]
        zs = []

        for weight, bias in zip(self.weights, self.biases):
            z = np.dot(weight, x) + bias
            zs.append(z)
            x = self.activation_function(z)
            activations.append(x)
            self.assert_nan(x, activations, zs)

        return x, activations, zs

    def backward_propagation(self, y_true, y_pred, activations, zs):
        grad_weights = [np.zeros(w.shape) for w in self.weights]
        grad_biases = [np.zeros(b.shape) for b in self.biases]

        delta = 2 * (y_pred - y_true) * self.activation_derivative(zs[-1])
        # delta = (y_pred - y_true)
        grad_biases[-1] = delta
        grad_weights[-1] = np.dot(delta, activations[-2].T)

        for l in range(2, len(self.layers)):
            delta = np.dot(self.weights[-l + 1].T, delta)
            # delta = np.dot(self.weights[-l + 1].T, delta) * self.activation_derivative(zs[-l])
            grad_biases[-l] = delta
            grad_weights[-l] = np.dot(delta, activations[-l - 1].T)

        return grad_weights, grad_biases

    def update_parameters(self, grad_weights, grad_biases, learning_rate):
        self.weights = [w - learning_rate * gw for w, gw in zip(self.weights, grad_weights)]
        self.biases = [b - learning_rate * gb for b, gb in zip(self.biases, grad_biases)]

    def assert_nan(self, x, activations, zs):
        if _assert_nan:
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

    def train(self, X, y, epochs, learning_rate=0.01, patience_limit=500, warm_up_epochs=500):
        best_val_loss = float('inf')
        patience_counter = 0

        for epoch in range(epochs):

            for x_val, y_val in zip(X, y):
                # sometimes storing the zs is useful for backpropagation. So, predict returns it
                # but we don't need it here
                y_pred, activations, zs = self.predict(x_val)
                loss = self.mse(y_val, y_pred)
                grad_weights, grad_biases = self.backward_propagation(y_val, y_pred, activations, zs)
                self.update_parameters(grad_weights, grad_biases, learning_rate)

            if epoch % 10 == 0:
                print(f"Epoch {epoch}, Loss: {loss}")

            if epoch >= warm_up_epochs:

                if loss < best_val_loss:
                    best_val_loss = loss
                    patience_counter = 0  # Reset counter
                else:
                    patience_counter += 1  # Increment counter

                if patience_counter >= patience_limit:
                    print("Early stopping due to lack of improvement.")
                    break


# Generate data
def generate_data(num_samples=1000):
    X = np.random.rand(num_samples)
    y = X * 100
    return X, y


def generate_apartment_data(num_samples=1000):
    # Initialize empty lists to hold our features and labels
    square_feet = []
    num_bedrooms = []
    num_bathrooms = []
    proximity_to_transit = []
    neighborhood_quality = []
    labels = []

    # Generate features and labels
    for _ in range(num_samples):
        square_feet.append(np.random.randint(500, 3001))
        num_bedrooms.append(np.random.randint(0, 5))
        num_bathrooms.append(np.random.randint(1, 4))
        proximity_to_transit.append(np.random.randint(1, 11))
        neighborhood_quality.append(np.random.randint(1, 11))

        # Calculate label (price) based on the features
        base_price = (square_feet[-1] * 1.5) + (num_bedrooms[-1] * 300) + (num_bathrooms[-1] * 200) + (
                proximity_to_transit[-1] * 40) + (neighborhood_quality[-1] * 50)

        # Add random fluctuation between 0-10%
        fluctuation = np.random.uniform(0, 0.1)
        final_price = base_price * (1 + fluctuation)

        labels.append(final_price)

    if num_samples > 1:
        # Scale each feature
        square_feet = MultiLevelPerceptron.minmax_scale(np.array(square_feet), np.min(square_feet), np.max(square_feet))
        num_bedrooms = MultiLevelPerceptron.minmax_scale(np.array(num_bedrooms), np.min(num_bedrooms),
                                                         np.max(num_bedrooms))
        num_bathrooms = MultiLevelPerceptron.minmax_scale(np.array(num_bathrooms), np.min(num_bathrooms),
                                                          np.max(num_bathrooms))
        proximity_to_transit = MultiLevelPerceptron.minmax_scale(np.array(proximity_to_transit),
                                                                 np.min(proximity_to_transit),
                                                                 np.max(proximity_to_transit))
        neighborhood_quality = MultiLevelPerceptron.minmax_scale(np.array(neighborhood_quality),
                                                                 np.min(neighborhood_quality),
                                                                 np.max(neighborhood_quality))
        labels = MultiLevelPerceptron.minmax_scale(labels, np.min(labels), np.max(labels))

    # Assemble features back into a single array
    features = np.column_stack((square_feet, num_bedrooms, num_bathrooms, proximity_to_transit, neighborhood_quality))

    return np.array(features), np.array(labels)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", default="simple",
                        help="simple for our basic * by 100 experiment. complex for our mock-housing example")

    args = parser.parse_args()

    if args.type == "simple":
        X, y = generate_data()

        X, y = MultiLevelPerceptron.scale_data(X, y)

        # Initialize and train the neural network
        mlp = MultiLevelPerceptron([1, 4, 3, 2, 1])
        mlp.activation_function = mlp.linear
        mlp.activation_derivative = mlp.linear_derivative
        X_test, y_test = generate_data(num_samples=1)
        print("Untrained: we generated:  ", X_test, ". We expect:", y_test, " but we predicted:",
              mlp.predict(X_test)[0])

        print("Let's train! ")
        mlp.train(X, y, epochs=1000, learning_rate=0.01)

        print("We're trained, let's predict again!")
        # Test the trained network
        for i in range(0, 10):
            X_test, y_test = generate_data(num_samples=1)
            print("Trained: we generated: ", X_test, ". We expect:", y_test, " and we predicted:",
                  mlp.predict(X_test)[0])

    elif args.type == "complex":
        # 5 inputs, 1 output
        mlp = MultiLevelPerceptron([5, 10, 25, 10, 1])

        # Generate data
        X, y = generate_apartment_data(num_samples=1)

        print("Untrained: we generated an apartment of:  ", X, ". We expect price:", y, " but we predicted:",
              mlp.predict(X)[0])

        print("Let's train! ")
        X, y = generate_apartment_data(num_samples=10000)

        mlp.train(X, y, epochs=10000, patience_limit=1000)
        print("We're trained, let's predict again!")
        for i in range(0, 10):
            X_test, y_test = generate_apartment_data(num_samples=1)
            print("Trained: we generated an apartment of:  ", X_test, ". We expect price:", y_test,
                  " but we predicted:",
                  mlp.predict(X_test)[0])

    else:
        print(f"I'm not sure what to do with type: {args.type}. Values are: simple or complex")
