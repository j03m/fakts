import numpy as np


# Activation function and its derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


# Generate synthetic data for training: Sort the sequences this time
def generate_data(num_samples=1000, seq_len=3):
    X = np.random.randint(1, 10, size=(num_samples, seq_len))
    y = np.array([sorted(x) for x in X])
    return minmax_scale(X), minmax_scale(y)


# Min-Max scaling
def minmax_scale(data, min_val=1, max_val=9):
    return (data - min_val) / (max_val - min_val)


# Mean Squared Error loss function
def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)


# Multi-layer Perceptron for encoder and decoder
def mlp_forward_pass(input_data, weights, biases, activation_func):
    layers = len(weights)
    activations = [input_data]

    for i in range(layers):
        z = np.dot(weights[i], activations[-1]) + biases[i]
        a = activation_func(z)
        activations.append(a)

    return activations


# Modifying backpropagate function to correct the shape issue by transposing the weight gradient
def backpropagate_fixed_v2(activations, weights, biases, loss_gradient, learning_rate):
    delta = [loss_gradient * sigmoid_derivative(activations[-1])]
    weight_gradients = []
    bias_gradients = []

    for j in range(len(weights) - 1, -1, -1):
        weight_gradient = np.outer(activations[j], delta[-1])
        bias_gradient = delta[-1]
        delta.append(np.dot(weights[j].T, delta[-1]) * sigmoid_derivative(activations[j]))

        weight_gradients.append(weight_gradient)
        bias_gradients.append(bias_gradient)

    # Update weights and biases in reverse order
    for j in range(len(weights) - 1, -1, -1):
        weights[j] -= learning_rate * weight_gradients[len(weights) - 1 - j].T
        biases[j] -= learning_rate * bias_gradients[len(weights) - 1 - j]

    return weights, biases, delta


# Replacing the original backpropagate with the fixed version in training function
def train_mlp_encoder_decoder_fixed_v2(epochs=1000, num_samples=1000, seq_len=3, learning_rate=0.1):
    encoder_weights = [np.random.rand(5, seq_len), np.random.rand(2, 5)]
    decoder_weights = [np.random.rand(5, 2), np.random.rand(seq_len, 5)]

    encoder_biases = [np.random.rand(5), np.random.rand(2)]
    decoder_biases = [np.random.rand(5), np.random.rand(seq_len)]

    X, y = generate_data(num_samples, seq_len)

    for epoch in range(epochs):
        total_loss = 0

        for i in range(num_samples):
            input_seq = X[i]
            target_seq = y[i]

            encoder_activations = mlp_forward_pass(input_seq, encoder_weights, encoder_biases, sigmoid)
            context_vector = encoder_activations[-1]

            decoder_activations = mlp_forward_pass(context_vector, decoder_weights, decoder_biases, sigmoid)
            output_seq = decoder_activations[-1]

    return encoder_weights, encoder_biases, decoder_weights, decoder_biases
# Train the model
encoder_weights, encoder_biases, decoder_weights, decoder_biases = train_mlp_encoder_decoder_fixed_v2()

input_seq, expectation = generate_data(1)

encoder_activations = mlp_forward_pass(input_seq, encoder_weights, encoder_biases, sigmoid)
context_vector = encoder_activations[-1]

decoder_activations = mlp_forward_pass(context_vector, decoder_weights, decoder_biases, sigmoid)
output_seq = decoder_activations[-1]

print("output:", output_seq, "expectation:", expectation)