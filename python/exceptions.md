Error and exception handling is a crucial aspect of robust software development. In Python, this is achieved through the use of `try`, `except`, `finally`, and `raise` statements, as well as the creation of custom exceptions. Here's a guide to understanding these concepts:

### 7. **Error and Exception Handling in Python**

#### a. **`try`, `except`, `finally`, and `raise`**

##### **1. `try` and `except` Blocks**
The `try` block contains code that might cause an exception, and the `except` block contains code that handles the exception.

**Example:**
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Division by zero!")
```

You can catch multiple exceptions by using multiple `except` blocks or a tuple of exceptions.

**Example:**
```python
try:
    # Code that might cause an exception
except (TypeError, ValueError):
    # Handle multiple exceptions
```

##### **2. `finally` Block**
The `finally` block contains code that will always be executed, whether an exception occurred or not.

**Example:**
```python
try:
    # Code that might cause an exception
finally:
    print("This will always be executed.")
```

##### **3. `raise` Statement**
The `raise` statement allows you to manually raise an exception.

**Example:**
```python
if value < 0:
    raise ValueError("Value must be non-negative")
```

#### b. **Creating Custom Exceptions**
You can create custom exceptions by defining a new class that inherits from Python's built-in `Exception` class or one of its derived classes.

**Example:**
```python
class MyCustomError(Exception):
    def __init__(self, message="A custom error occurred"):
        super().__init__(message)
```

You can then raise this custom exception using the `raise` statement.

**Example:**
```python
raise MyCustomError("Something went wrong")
```
