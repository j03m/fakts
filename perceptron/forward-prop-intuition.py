import numpy as np

# Function for the sigmoid activation
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Initialize input (3 neurons)
X = np.array([[0.1], [0.2], [0.3]])  # 3x1 matrix

# Initialize weight matrix (2x3)
W = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])  # 2x3 matrix

# Initialize bias (2 neurons)
b = np.array([[0.1], [0.2]])  # 2x1 matrix

# Perform forward propagation
Z = np.dot(W, X) + b  # Z = WX + b
Y = sigmoid(Z)  # Activation

# Print each step for visualization
print(f"Input (X) shape: {X.shape}\n{X}")
print(f"Weight (W) shape: {W.shape}\n{W}")
print(f"Bias (b) shape: {b.shape}\n{b}")
print(f"Weighted sum (Z) shape: {Z.shape}\n{Z}")
print(f"Output (Y) shape: {Y.shape}\n{Y}")
