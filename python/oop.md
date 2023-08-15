### 5. **Object-Oriented Programming (OOP) in Python**

#### a. **Classes and Objects**
Python classes are defined using the `class` keyword, and objects are instances of classes.

**Example:**
```python
class MyClass:
    def __init__(self, value):
        self.value = value

obj = MyClass(5)
```

#### b. **Inheritance and Polymorphism**
Python supports single and multiple inheritance, allowing for code reuse and polymorphism.

**Example of Inheritance:**
```python
class Parent:
    pass

class Child(Parent):
    pass
```

**Example of Polymorphism:**
```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof"

class Cat(Animal):
    def speak(self):
        return "Meow"
```

#### c. **Encapsulation and Abstraction**
Encapsulation is achieved by using private attributes and methods (prefixing with an underscore). Abstraction can be implemented using abstract classes.

**Example of Encapsulation:**
```python
class Encapsulated:
    def __init__(self):
        self._private_var = 5
```

**Example of Abstraction:**
```python
from abc import ABC, abstractmethod

class AbstractClass(ABC):
    @abstractmethod
    def abstract_method(self):
        pass
```

#### d. **Magic Methods and Operator Overloading**

Magic methods, also known as dunder methods (double underscore), allow you to define how objects behave with operators and built-in functions.

##### **1. Constructor and Destructor**
```python
class MyClass:
    def __init__(self, value):  # Constructor
        self.value = value

    def __del__(self):  # Destructor
        print("Object destroyed")
```

##### **2. String Representation**
```python
class MyClass:
    def __str__(self):  # Human-readable representation
        return "MyClass object"

    def __repr__(self):  # Unambiguous representation
        return f"MyClass(value={self.value})"
```

##### **3. Arithmetic Operators**
```python
class Vector:
    def __add__(self, other):  # Addition
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):  # Subtraction
        return Vector(self.x - other.x, self.y - other.y)
```

##### **4. Comparison Operators**
```python
class MyClass:
    def __eq__(self, other):  # Equal to
        return self.value == other.value

    def __lt__(self, other):  # Less than
        return self.value < other.value
```

##### **5. Context Managers**
```python
class MyContext:
    def __enter__(self):
        print("Entering context")

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting context")
```

#### All Dunder methods:

Below is an exhaustive list of some commonly used dunder (double underscore) or magic methods in Python, along with their descriptions and examples.

### 1. **Object Creation and Destruction**
- `__new__(cls, ...)`: Called before `__init__` to create a new instance. Rarely used.
- `__init__(self, ...)`: Constructor, used to initialize the object.
- `__del__(self)`: Destructor, called when the object is about to be destroyed.

### 2. **String Representation**
- `__str__(self)`: Returns a human-readable string representation.
- `__repr__(self)`: Returns an unambiguous string representation, often used for debugging.

### 3. **Arithmetic Operators**
- `__add__(self, other)`: Defines addition (`+`).
- `__sub__(self, other)`: Defines subtraction (`-`).
- `__mul__(self, other)`: Defines multiplication (`*`).
- `__truediv__(self, other)`: Defines division (`/`).
- `__floordiv__(self, other)`: Defines floor division (`//`).
- `__mod__(self, other)`: Defines the modulo operator (`%`).
- `__pow__(self, other)`: Defines the power operator (`**`).

### 4. **In-Place Arithmetic Operators**
- `__iadd__(self, other)`: Defines in-place addition (`+=`).
- `__isub__(self, other)`: Defines in-place subtraction (`-=`).
- `__imul__(self, other)`: Defines in-place multiplication (`*=`).
- `__itruediv__(self, other)`: Defines in-place division (`/=`).

### 5. **Comparison Operators**
- `__eq__(self, other)`: Defines equality (`==`).
- `__ne__(self, other)`: Defines inequality (`!=`).
- `__lt__(self, other)`: Defines less than (`<`).
- `__le__(self, other)`: Defines less than or equal to (`<=`).
- `__gt__(self, other)`: Defines greater than (`>`).
- `__ge__(self, other)`: Defines greater than or equal to (`>=`).

### 6. **Attribute Access**
- `__getattr__(self, name)`: Called when an attribute is not found.
- `__setattr__(self, name, value)`: Called when setting an attribute.
- `__delattr__(self, name)`: Called when deleting an attribute.

### 7. **Container Types**
- `__len__(self)`: Returns the length of the container.
- `__getitem__(self, key)`: Accesses an item using square brackets.
- `__setitem__(self, key, value)`: Sets an item using square brackets.
- `__delitem__(self, key)`: Deletes an item using square brackets.
- `__contains__(self, item)`: Checks if an item is in the container.

### 8. **Context Managers**
- `__enter__(self)`: Enters a context (used with `with` statement).
- `__exit__(self, exc_type, exc_value, traceback)`: Exits a context.

### 9. **Callable Objects**
- `__call__(self, ...)`: Allows an instance to be called as a function.

### 10. **Miscellaneous**
- `__hash__(self)`: Returns the hash value of the object.
- `__format__(self, format_spec)`: Customizes string formatting.
- `__dir__(self)`: Customizes the result of the `dir()` function.

### Example Usage
Here's an example of how you might use some of these methods in a custom class:

```python
class ComplexNumber:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __str__(self):
        return f"{self.real} + {self.imag}i"

    def __add__(self, other):
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __call__(self):
        return f"Called a ComplexNumber with value {self.real} + {self.imag}i"
```

These magic methods allow you to define custom behaviors for objects, making your classes more expressive and Pythonic. They enable operator overloading, custom string representations, and more, providing a rich set of tools for object-oriented programming.
