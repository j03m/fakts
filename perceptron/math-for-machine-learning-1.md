# Math For Machine Learning 1

This article will review the various bits of math required to fully grasping
what is happening in the [Multi-layered Perceptron (MLP)](./perceptron.md) 
chapter. The MLP will form the foundation for the other chapters in this book
but purposes glosses over some of the mathmetics to help the reader fully grasp
conceptually what is happening in the perceptron code without getting lost in
the mechanics of partial derivatives and matrix transformations.

However, in order to really progress in the field and to be able to digest and more
importantly, debug some of the issue that arise in the field and understanding of the 
math is important. 

Notably, this will cover the math from the MLP chapter. As we encounter new concepts
in the other chapters, we will introduce additional mathmatics chapters separately
from our implementations so that they can be referred to after an initial intuition
is made.

## MSE - Mean Squared Error

In our perceptron model, we employ the concept of Mean Squared Error (MSE) to quantify the network's loss. By "loss," we refer to the discrepancy between a given prediction and the actual, or true, value.

Mathematically, the MSE is defined as:

$$\[
\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_{\text{true}, i} - y_{\text{pred}, i})^2
\]$$

Where $$\( n \)$$ is the number of samples.

In Python, this formula can be implemented as follows:

```python
@staticmethod
def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)
```

Here's a quick example to illustrate the calculation:

```python
>>> y_true = [5, 6, 7, 8]  # Desired result
>>> y_pred = [10, 6, 4, 8] # Predicted result
>>> (np.array(y_true) - y_pred) # Differences
array([-5,  0,  3,  0])
>>> (np.array(y_true) - y_pred) ** 2 # Squaring the differences
array([25,  0,  9,  0])
>>> np.mean((np.array(y_true) - y_pred) ** 2) # Mean of squared differences
8.5
```

### Breaking Down the Equation Components

Let's break down the components of the MSE formula for a deeper understanding:

- $\( \text{MSE} \)$: This is the Mean Squared Error, which serves as a measure of how well the model's predictions match the true values.
  
- $\( \frac{1}{n} \)$: This part represents the average. We sum up all the squared differences and then divide by $\( n \)$, the number of samples, to get an average.

- $\( \sum_{i=1}^{n} \)$: This is the summation notation, indicating that we sum up the squared differences for each sample from $\( i = 1 \) to \( n \)$.

- $\( (y_{\text{true}, i} - y_{\text{pred}, i})^2 \)$: This part calculates the squared difference between the true value $\( y_{\text{true}, i} \)$ and the predicted value $\( y_{\text{pred}, i} \)$ for each sample $\( i \)$.

By understanding each component, you can better appreciate how MSE provides a comprehensive measure of the model's performance. It squares the differences to eliminate negative values, sums them up, and then averages them to get a single value that can be minimized during the training process.

## Derivative

#### Intuition

Imagine driving a car on a hilly road. The derivative would tell you how steep the hill is at each point. If the derivative is zero, you're at a flat point, possibly the top or bottom of a hill.

## Partial Derivative

In multivariable calculus, when a function depends on more than one variable, we use partial derivatives. A partial derivative with respect to one variable tells us how the function changes with respect to that variable, keeping all other variables constant.

### Intuition

Let's say you're playing minecraft, and you're in a mountain range. The mountains extend descend in different directions. Depending on the direction you move in, you might move up or down. In a Minecraft mountain range, each point in the terrain can be represented by coordinates $\( (x, y, z) \)$, where $\( x \)$ and $\( y \)$ are the horizontal coordinates and $\( z \)$ is the elevation. 

If you're standing at a particular point $\( (x_0, y_0, z_0) \)$, a partial derivative with respect to $\( x \)$ would tell you how much the elevation $\( z \)$ changes as you move in the $\( x \)$-direction, while keeping $\( y \)$ constant. Similarly, the partial derivative with respect to $\( y \)$ would tell you how $\( z \)$ changes as you move in the $\( y \)$-direction, keeping $\( x \)$ constant.

So, if $\( \frac{\partial z}{\partial x} \)$ is positive at $\( (x_0, y_0, z_0) \)$, it means that moving in the positive $\( x \)$-direction will increase your elevation, i.e., you'll be moving uphill. If it's negative, you'll be moving downhill. The same logic applies for $\( \frac{\partial z}{\partial y} \)$.

In the context of neural networks, each weight and bias can be thought of as a coordinate in a high-dimensional space, and the partial derivatives help us understand how the error changes as we tweak each of these parameters.