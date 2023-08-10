Lambda expressions and closures are powerful features in C++ that enable concise and flexible function-like behavior. Let's explore these concepts in detail:

### Lambda Expressions

A lambda expression in C++ is an anonymous function or a function without a name. It can take input parameters, return values, and can be used just like regular functions.

#### Syntax

Here's the general syntax of a lambda expression:

```cpp
[capture](parameters) -> return_type { body_of_lambda }
```

- **Capture**: Defines what external variables are available for the lambda.
- **Parameters**: A list of parameters just like regular functions.
- **Return Type**: Optional, and if skipped, it's inferred from the return statements in the lambda.
- **Body of Lambda**: The code that gets executed when the lambda is called.

#### Example

```cpp
auto add = [](int a, int b) -> int { return a + b; };
int sum = add(3, 4); // sum is 7
```

### Capture Modes

The capture clause defines how the lambda can access variables from the enclosing scope.

- **`[=]`**: Capture all local variables by value.
- **`[&]`**: Capture all local variables by reference.
- **`[a, &b]`**: Capture `a` by value and `b` by reference.
- **`[]`**: Capture nothing.

### Closures

A closure is an instance of a lambda expression. It's a function object that, in addition to code, contains references or copies of local variables from the surrounding scope. These captured variables allow the lambda to have state.

#### Example with State

```cpp
int a = 5;
auto add_a = [a](int b) { return a + b; }; // 'add_a' is a closure
int result = add_a(3); // result is 8
```

### Mutable Lambdas

By default, variables captured by value are const within the lambda. If you want to modify them within the lambda, you can use the `mutable` keyword.

```cpp
int count = 0;
auto increment = [count]() mutable { count++; };
increment(); // 'count' within the lambda is modified, but the external 'count' is still 0
```

### Generic Lambdas (C++14 and later)

C++14 introduced generic lambdas, allowing auto type for parameters, enabling more generic code.

```cpp
auto multiply = [](auto a, auto b) { return a * b; };
```

### Conclusion

Lambda expressions and closures provide a concise and flexible way to define functions inline, often used for short snippets of code that are passed to algorithms or used for callbacks.

- **Lambda Expressions**: Enable anonymous functions with captures to access outer scope.
- **Closures**: Instances of lambdas that can maintain state.
- **Capture Modes**: Control how variables from the enclosing scope are accessed.

### Templates

Starting with C++20, you can have template lambdas. This feature allows you to define a lambda expression with template parameters, making it even more powerful and flexible.

### Syntax

Here's the general syntax of a template lambda:

```cpp
[capture]<typename T>(T parameter) { body_of_lambda }
```

### Example

Here's an example of a template lambda that can accept parameters of any type and print them:

```cpp
auto printValue = []<typename T>(T value) { std::cout << value << '\n'; };

printValue(42);        // prints an integer
printValue(3.14);      // prints a double
printValue("hello");   // prints a string
```

### Combining with Auto Parameters

You can also combine template lambdas with auto parameters for more concise syntax:

```cpp
auto multiply = []<typename T>(T a, auto b) { return a * b; };

int result = multiply<int>(3, 4.5); // result is 13.5
```

### Nested Template Lambdas

Template lambdas can also be nested within other lambdas, allowing for more complex and generic behaviors:

```cpp
auto outerLambda = []<typename T>(T value) {
    return [value]<typename U>(U multiplier) { return value * multiplier; };
};

auto innerLambda = outerLambda<int>(5);
int result = innerLambda<double>(2.5); // result is 12.5
```

Here's an example that includes both template parameters and captures in a lambda expression:

```cpp
int multiplier = 3;

auto multiplyByFactor = [multiplier]<typename T>(T value) {
    return value * multiplier;
};

int result1 = multiplyByFactor(5);   // result1 is 15
double result2 = multiplyByFactor(4.5); // result2 is 13.5
```

In this example, the lambda expression captures the `multiplier` variable from the surrounding scope and also defines a template parameter `T`. This allows the lambda to accept arguments of any type and multiply them by the captured `multiplier`.

The combination of captures and template parameters in lambda expressions provides a powerful way to write generic and flexible code that can adapt to different types while still interacting with the surrounding context.