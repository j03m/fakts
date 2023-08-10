### Object-Oriented Programming (OOP) in C++

#### 1. Classes and Objects
- **Classes**: A class is a blueprint for creating objects. It defines the properties (attributes) and behaviors (methods) that the objects created from the class will have.
- **Objects**: An object is an instance of a class. It represents a specific realization of the class, with its own set of values for the attributes defined in the class.

Example:
```cpp
class Car {
public:
    std::string make;
    std::string model;
    int year;
    
    void start() {
        std::cout << "Car started!\n";
    }
};

Car myCar; // Creating an object of the Car class
myCar.make = "Toyota";
myCar.model = "Camry";
myCar.year = 2020;
myCar.start(); // Output: Car started!
```

#### 2. Inheritance
- **Inheritance**: This allows a class to inherit attributes and methods from another class. It promotes code reusability and establishes a relationship between the parent (base) class and the child (derived) class.

Example:
```cpp
class Vehicle {
public:
    std::string brand;
    void honk() {
        std::cout << "Honk!\n";
    }
};

class Car : public Vehicle { // Car inherits from Vehicle
public:
    std::string model;
};

Car myCar;
myCar.brand = "Ford";
myCar.model = "Mustang";
myCar.honk(); // Output: Honk!
```

#### 3. Polymorphism
- **Polymorphism**: This allows objects of different classes to be treated as objects of a common base class. It enables one interface to be used for a general class of actions, making the code more flexible and extensible.

Example (using virtual functions for runtime polymorphism):
```cpp
class Shape {
public:
    virtual void draw() { // Virtual function
        std::cout << "Drawing Shape\n";
    }
};

class Circle : public Shape {
public:
    void draw() override { // Overriding the base class method
        std::cout << "Drawing Circle\n";
    }
};

Shape* shape = new Circle();
shape->draw(); // Output: Drawing Circle
```

#### 4. Encapsulation
- **Encapsulation**: This involves bundling the data (attributes) and the methods that operate on the data into a single unit (class) and restricting access to some of the object's components. It enhances security and integrity by using access specifiers like `public`, `private`, and `protected`.

Example:
```cpp
class BankAccount {
private:
    double balance;

public:
    void deposit(double amount) {
        balance += amount;
    }

    double getBalance() {
        return balance;
    }
};
```

#### 5. Operator Overloading
- **Operator Overloading**: This allows you to redefine the way operators work for user-defined types (classes). It enhances code readability and allows intuitive mathematical operations on objects.

Example:
```cpp
class Complex {
public:
    double real, imag;

    Complex operator + (const Complex& other) {
        Complex result;
        result.real = real + other.real;
        result.imag = imag + other.imag;
        return result;
    }
};
```

#### 6. Friend Functions
- **Friend Functions**: These are functions that are not members of a class but can access the private and protected members of the class. They are declared with the `friend` keyword inside the class.

Example:
```cpp
class Box {
private:
    int length;

public:
    friend void displayLength(Box& box); // Friend function declaration
};

void displayLength(Box& box) {
    std::cout << "Length: " << box.length << "\n"; // Accessing private member
}
```

These concepts form the core of OOP in C++ and are essential for building robust and maintainable software systems. Understanding and applying these principles will enable you to design classes and objects that model real-world entities, promote code reusability, and enhance code maintainability.

