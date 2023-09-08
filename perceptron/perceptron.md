# Multi-layered Perceptron (MLP)

An MLP is a type of neural network. In many contexts, the terms "Multi-layered Perceptron" and "neural network" can be used interchangeably. The MLP is often considered one of the simplest types of neural networks, making it an excellent starting point for understanding machine learning fundamentals.

The objective of this guide is not to build a production-quality neural network or even a particularly robust example. Instead, we aim to demonstrate the core principles that allow a neural network to learn and make predictions. By understanding these principles, you'll gain an intuitive grasp of the training process, which involves updating a model's weights and biases.

## What You Will Learn:

* The basic idea behind neural networks and MLPs
* The mechanics of forward and backward propagation
* How to train an MLP to make predictions

We will initially focus on the practical implementation, glossing over the mathematics involved. Once we've built a foundational understanding, we'll circle back to delve into the mathematical details, ensuring a comprehensive grasp of what happens at each step.

## Weights and Biases: The Tuning Knobs of a Neural Network

Training a neural network is sort of like tuning a guitar. You're going to make some minor adjustments to your strings until you get a specific note. 

At its most basic, numbers go into a neural network and are essentially run through a number of transformations. The original numerical values are augmented by weights and biases to achieve a specific result. An untrained neural network (i.e., one with randomly generated weights and biases) won't produce the results we want. But when these weights and biases are adjusted (a.k.a. tuned), we can eventually achieve the results we want.

In the neural network we're training we'll essentially train a network to 
multiply an input number by 100. That seems like an incredibly silly task, why would we 
do that if we could just do `i * 100`, but this silly task actually demonstrates the
power for weights and biases. You see, we'll demonstrate that given a random set of
weights and a random set of biases and a series of examples that we can tune these
augmentation such that our network can be made to predict what `i * 100` would produce.

### What are Weights?

Weights are the strength of the connections between neurons in different layers of the network. You can think of them as the influence one neuron has over the next. In a mathematical sense, each weight represents the multiplier for an input value. 

For example, consider a simple equation for a straight line \( y = mx + b \). Here, \( m \) would be akin to the weight—it determines how much \( x \) influences \( y \).

### What are Biases?

Biases allow neurons to have some flexibility in activation. In the straight line equation \( y = mx + b \), the \( b \) term serves as a bias, shifting the line up or down.

### Why are they important?

Weights and biases are crucial because they are what the neural network adjusts during learning. Through a process called backpropagation, which we'll cover later, the network tweaks these parameters to minimize the difference between its predictions and the actual data. As these "tuning pegs" get adjusted, the network becomes better at its task.

Absolutely, introducing the code early on can set the context for the reader and allow them to know where to look for practical examples as they go through the article. You can introduce the code in a concise yet informative manner.

### Introducing the Code

All the concepts discussed in this article are accompanied by a practical Python example [mlp.py](mlp.py), which is in this repo and introduces a neural network we used to demonstrate that we could train it multiply by 100.

The Python file contains a class named `MultiLevelPerceptron`, which serves as our neural network model for this tutorial. While we'll go into detail about how the code works later on, for those who like to jump ahead or want a sneak peek, feel free to explore this file.

The class encapsulates all the functionalities we're going to discuss, from initializing weights and biases to performing forward and backward propagation. By the end of this article, you'll understand how every line of this code contributes to the learning process of the neural network.

While we'll reference snippets here, you should definitely clone the repo and give the file a run.

#### The Constructor

The constructor of our `MultiLevelPerceptron` class takes an array of integers called `layers`, which specifies the number of neurons in each layer of the neural network. 

For example, to predict our multiplied input, we create an instance of the MLP class like this:

```python
mlp = MultiLevelPerceptron([1, 4, 3, 2, 1])
```

These numbers aren't arbitrary. The first and last layers have only 1 neuron because we're transforming one number (our input) into another number (our output). The middle layers, represented by `4, 3, 2`, are designed to introduce some complexity into the network. This complexity helps the network learn more intricate patterns, allowing for better predictions without taking too much time to train. You can think of more complexity basically meaning more variables. In the same way that multivariate equations can represent more complex geometric patterns, more variables (or neurons in this case) allow networks to make more intricate connections about data. As a result, the network can make more advanced predictions.

Internally, the constructor does the following:

1. Captures the `layers` array to set the architecture.
2. Initializes empty lists for `weights` and `biases` that will be filled later.
3. Sets an activation function, `self.linear` in this case (we'll discuss activation functions in detail later).
4. Calls the `_initialize_weights_and_biases()` method to actually set the initial random weights and zero biases.

Here's the code snippet for the constructor:

```python
class MultiLevelPerceptron:
    def __init__(self, layers):
        self.layers = layers
        self.weights = []
        self.biases = []
        self.activation_function = self.linear
        self._initialize_weights_and_biases()
```

#### The Initialization

Initialization sets up our weights and biases. To understand what's happening here, we need to cover some basics. We discussed earlier that the network essentially augments our input. How does it do that? Through matrix operations.

When the input is provided, its value will be augmented by each neuron in the next layer. Here's a basic diagram to help illustrate this concept:

![First Layer Connections](first-layer.png)

Imagine we have a layer configuration `[1, 4, 3, 2, 1]`, as in our example. The weight matrix for the transition from the input layer with 1 neuron to the first hidden layer with 4 neurons would look something like this:

<p>
  <strong>Weight Matrix 1</strong> = 
  <span style="font-family: 'Courier New', Courier, monospace;">[w<sub>11</sub>]</span>
  &rarr;
  <span style="font-family: 'Courier New', Courier, monospace;">[w<sub>21</sub>, w<sub>22</sub>, w<sub>23</sub>, w<sub>24</sub>]</span>
</p>

This is a matrix of dimensions `1 x 4`.

The next transition, from the first hidden layer with 4 neurons to the second hidden layer with 3 neurons, would have a Weight Matrix of dimensions `4 x 3`. 

<!-- Weight Matrix 2 HTML Representation -->

<p>
  <span style="font-family: 'Courier New', Courier, monospace;">Weight Matrix 2 = </span>
  <span style="font-size: 1.2em;">
    [
    <span style="vertical-align: 0.5em;">
      <table style="display: inline-table; margin: 0; padding: 0; border: none;">
        <tr>
          <td style="border: none;">w<sub>21</sub></td>
          <td style="border: none;">w<sub>22</sub></td>
          <td style="border: none;">w<sub>23</sub></td>
        </tr>
        <!-- ... rest of the matrix -->
      </table>
    ]
  </span>
</p>

We use `np.random.randn` to initialize these weights randomly, which is a common practice in neural network training. According to the numpy documentation, `np.random.randn` generates an array filled with random floats sampled from a Gaussian distribution with mean 0 and variance 1. 

Here's how you can generate such matrices in Python:

```python
import numpy as np
np.random.randn(4, 1)
np.random.randn(3, 4)
```

Here is what that looks like in the repl:

```python
>>> import numpy as np
>>> np.random.randn(4, 1)
array([[-0.79168001],
       [-0.49160509],
       [-1.57004755],
       [-1.16798333]])

>>> np.random.randn(3, 4)
array([[ 0.92383058, -0.53372624,  0.39269497, -2.23828113],
       [-0.53587544,  0.17031796, -0.62955261,  0.42078053],
       [ 0.74553714, -0.25580175, -0.65622554,  0.7881166 ]])
```

Think of each weight as a "pathway" for information flow between two neurons in adjacent layers. The matrix is essentially a structured way to store all these different pathways. The number of rows in the Weight Matrix corresponds to the neurons in the layer we're transitioning to, and the number of columns corresponds to the neurons in the layer we're transitioning from. This setup is because each neuron in the next layer is connected to every neuron in the previous layer.

In our code, biases are initialized to zero. This is a common practice and generally works well for small networks like the one we're working with.

Up next, we'll see how this all comes together in forward propagation.

Certainly, adding a brief section on activation functions can clarify why a linear function was chosen in this specific example while also briefly touching on other types of activation functions like the sigmoid.

---

#### A Note on Activation Functions

In our example, we're using a linear activation function. That's simply because our task is to perform a linear transformation on the input—multiplying it by 100. A linear activation function does nothing to the weighted sum `z`, effectively leaving it unchanged:

<p>
  <strong>Linear Function: </strong>
  f(x) = x
</p>


However, not all tasks are best suited for a linear activation function. For instance, in classification tasks, the sigmoid activation function is often used. The sigmoid function maps any input into a value between 0 and 1, which can be useful for probabilities:

<p>
  <strong>Sigmoid Function: </strong>
  &#963;(z) = 1 / (1 + e<sup>-z</sup>)
</p>

The choice of activation function can greatly influence a neural network's performance and is usually tailored to the specific problem you're trying to solve.

#### Forward Propagation: Making Predictions

Forward propagation is the process by which a neural network makes a prediction based on input data. It's called "forward" because we pass the data through the network in a single direction, from the input layer all the way through to the output layer.

##### The Function Signature

The `predict` function takes a single argument `x`, which is our single random number. We want the network to essentially
multiply this number by 100 when it makes its prediction.

```python
def predict(self, x):
```

##### Preparing the Input

The first line inside the function reshapes the input `x` into a column vector. This ensures that the input is compatible with the weight matrices for matrix multiplication.

```python
x = np.array(x).reshape(-1, 1)
```

##### Initializing Containers for Activations and "Z"s

The function also initializes two lists, `activations` and `zs`. The variable `z` often refers to the linear combination of the input features and the weights, before applying the activation function.

- `activations` keeps track of the output of each layer's neurons after applying the activation function. 
- `zs` stores the weighted sums before the activation function is applied at each layer.

```python
activations = [x]
zs = []
```

The first activation is simply `x`, our input number.

##### The Core Loop

Then, the function enters a loop that iterates through each layer of the network to perform the actual forward propagation.

```python
for weight, bias in zip(self.weights, self.biases):
```

For each layer, the code performs the following steps:

1. **Weighted Sum**: It multiplies the current `x` (activation from the previous layer) by the weight matrix and then adds the bias. This is the weighted sum `z`.

    ```python
    z = np.dot(weight, x) + bias
    ```
   
    The dot product (`np.dot`) here represents the sum of the products of corresponding entries of the two sequences of numbers. 

   For example remember our weight matrices from earlier? Our first iteration will combine our input with the first matrix, effectively, sending the output of the first layer to the second layer, and augmenting each value. 

   ```python
   >>> foo = np.random.randn(4, 1)
   >>> x
   array([[0.5]])
   >>> z = np.dot(foo, x) # bias not included for brevity
   >>> z
   array([[ 0.78350497],
       [ 0.0137708 ],
       [ 0.59015738],
       [-0.3671776 ]])
   ```
   > In the example using the dot product, note that this is a simplified example. In the actual code, biases are also added to each neuron's output.

   This then continues, where each subsequent activation is sent to the next layer to be augmented.

2. **Storing Z**: It appends this `z` to the `zs` list.

    ```python
    zs.append(z)
    ```

3. **Activation Function**: It then applies the activation function to `z` to get the next `x`, or the activation for the next layer. The activation function used here is the linear function, which essentially does nothing (i.e., \( f(x) = x \)).

    ```python
    x = self.activation_function(z)
    ```

4. **Storing Activation**: Finally, it appends this new `x` to the `activations` list.

    ```python
    activations.append(x)
    ```
   
##### Sanity Check for NaN

After the loop, the function performs a sanity check to make sure that no `NaN` (Not a Number) values have crept into the calculations. We will
talk more about why this is here later in exploding gradients and scaling

```python
self.assert_nan(x, activations, zs)
```

##### Returning the Output

Finally, the function returns the final `x` (the network's prediction), along with the `activations` and `zs` for each layer. These are not only useful for debugging but also critical for backpropagation.

```python
return x, activations, zs
```

Of course without training, the output of the net is going to be junk. For example, making a 
prediction as is looks like this:

```python
X, y = generate_data()

X, y = MultiLevelPerceptron.scale_data(X, y)

# Initialize and train the neural network
mlp = MultiLevelPerceptron([1, 4, 3, 2, 1])

#mlp.train(X, y, epochs=1000, learning_rate=0.01)

# Test the trained network
for i in range(0, 10):
    X_test, y_test = generate_data(num_samples=1)
    print("Generated: ", X_test, " expect:", y_test, " predict:", mlp.predict(X_test)[0])
```

Yields:

```
(venv) jmordetsky in ~/curriculum (main) > python3 perceptron/mlp.py 
Generated:  [0.20471242]  expect: [20.4712423]  predict: [[0.44438418]]
Generated:  [0.29994221]  expect: [29.99422076]  predict: [[0.65110642]]
Generated:  [0.20042107]  expect: [20.04210658]  predict: [[0.43506862]]
Generated:  [0.91912764]  expect: [91.91276357]  predict: [[1.99521737]]
Generated:  [0.89951592]  expect: [89.9515918]  predict: [[1.95264479]]
Generated:  [0.93948362]  expect: [93.94836198]  predict: [[2.03940559]]
Generated:  [0.45195635]  expect: [45.19563525]  predict: [[0.98109461]]
Generated:  [0.49573883]  expect: [49.57388271]  predict: [[1.07613642]]
Generated:  [0.64975961]  expect: [64.97596097]  predict: [[1.41048056]]
Generated:  [0.20056979]  expect: [20.05697901]  predict: [[0.43539147]]
```

Very clearly, this is not useful. But don't worry—this is entirely expected for a neural network that hasn't been trained yet. This leads us to our next step: training and backpropagation!

# Backpropagation

Earlier we said:

> At its most basic, numbers go into a neural network and are essentially run through a number of transformations. The original numerical values are augmented by weights and biases to achieve a specific result. An untrained neural network (i.e., one with randomly generated weights and biases) won't produce the results we want. But when these weights and biases are adjusted (a.k.a. tuned), we can eventually achieve the results we want.

Backpropagation is the process whereby those guitar knobs are tuned. When you are tuning a guitar you will pluck a string and an atuned musician will know which way to turn the knob based on the sound the strum produces. 

Backpropagation is like that for the neural network. It will examine the results of a prediction (a pluck of a string) and then adjust the weights and biases of the network in a direction that it believes will lead it to the correct answer, where the correct answer is the sample training data it is provided.

So, backpropagation is fundamentally an optimization algorithm for minimizing the error in the neural network's predictions.

There is a bunch of math concepts we're going to need to get comfortable with if we want to know how this stuff works. We don't need to solve any equations mind you, but it really helps to know the high level concepts.

In calculus, a derivative measures how a function changes as its input changes. In simpler terms, it tells us the "slope" or "rate of change" at a particular point. The mathematical notation for the derivative of a function is $\( f(x) \) is \( f'(x) \) or \( \frac{{d}}{{dx}} f(x) \).

