### 7. **File I/O and Streams**

#### a. File Operations with `fstream`

The `fstream` library in C++ provides functionalities to read from and write to files. It includes classes like `ifstream` for reading (input) and `ofstream` for writing (output).

##### i. Reading from a File

You can use the `ifstream` class to read from a file. Here's an example:

```cpp
#include <iostream>
#include <fstream>

int main() {
    std::ifstream file("example.txt");
    std::string line;

    if (file.is_open()) {
        while (std::getline(file, line)) {
            std::cout << line << '\n';
        }
        file.close();
    } else {
        std::cout << "Unable to open file";
    }

    return 0;
}
```

This code reads the content of "example.txt" line by line and prints it to the console.

##### ii. Writing to a File

The `ofstream` class is used to write to a file. Here's an example:

```cpp
#include <fstream>

int main() {
    std::ofstream file("output.txt");
    file << "Writing this to a file.\n";
    file.close();

    return 0;
}
```

This code writes a line to "output.txt". If the file doesn't exist, it will be created.

#### b. Stream Manipulators

Stream manipulators are used to control the formatting of output and input streams. They can be used to set precision, fill characters, alignment, etc.

Example:

```cpp
#include <iostream>
#include <iomanip>

int main() {
    double value = 123.456789;
    std::cout << std::fixed << std::setprecision(2) << value << '\n'; // Output: 123.46
    return 0;
}
```

Here, `std::fixed` and `std::setprecision(2)` are used to format the output to two decimal places.

#### c. Custom Stream Classes

You can create custom stream classes by inheriting from existing stream classes like `std::ostream` or `std::istream`. This allows you to define custom behaviors for reading and writing data.

Example:

```cpp
#include <iostream>
#include <sstream>

class CustomStream : public std::ostringstream {
public:
    CustomStream() {
        // Custom initialization
    }

    // Custom methods
};

int main() {
    CustomStream customStream;
    customStream << "Hello, Custom Stream!";
    std::cout << customStream.str() << '\n'; // Output: Hello, Custom Stream!
    return 0;
}
```

This example demonstrates a custom stream class that inherits from `std::ostringstream`. You can add custom methods and behaviors as needed.

### Real-World Applications

1. **File Operations**: Reading and writing files are common in applications like configuration management, data processing, and logging.
2. **Stream Manipulators**: Used in formatting reports, financial data, or any scenario where precise control over data formatting is required.
3. **Custom Stream Classes**: Useful in creating specialized logging systems, custom serialization/deserialization, or interfacing with unique data formats.

### Conclusion

File I/O and streams in C++ enable powerful interactions with the file system and provide control over data formatting. Understanding these concepts is essential for a wide range of applications, from simple data storage to complex data processing and manipulation.