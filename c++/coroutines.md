Let's explore a real-world example using C++20 coroutines with `co_yield`. We'll create a generator function that reads a large file line by line and yields each line to the caller. This can be useful in scenarios where you want to process a large file without loading the entire content into memory.

#### Code Example

```cpp
#include <iostream>
#include <fstream>
#include <string>
#include <experimental/coroutine>
#include <generator>

std::generator<std::string> read_file_line_by_line(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        co_return; // Exit the coroutine if the file couldn't be opened
    }

    std::string line;
    while (std::getline(file, line)) {
        co_yield line; // Yield each line to the caller
    }
}

int main() {
    for (const auto& line : read_file_line_by_line("large_file.txt")) {
        std::cout << line << '\n'; // Process each line
    }
    return 0;
}
```

#### Explanation

1. **Coroutine Function `read_file_line_by_line`:** This function takes a filename and returns a generator that yields each line of the file. It uses `std::ifstream` to open the file and `std::getline` to read it line by line.

2. **`co_yield`:** Inside the loop, the `co_yield` keyword is used to yield each line to the caller. This suspends the coroutine's execution and returns the line to the caller. The next time the caller requests a value, the coroutine resumes execution from where it left off.

3. **`co_return`:** If the file couldn't be opened, `co_return` is used to exit the coroutine.

4. **Main Function:** The main function uses a range-based `for` loop to iterate over the lines yielded by the coroutine. It prints each line to the standard output, but you could replace this with any processing logic you need.

This example illustrates how you can use C++20 coroutines with `co_yield` to create a lazy generator that reads a large file line by line. This can be a powerful tool in scenarios where you need to process large datasets efficiently.

Note: The code above uses features from the C++20 standard, so you'll need a compiler that supports C++20, and you may need to enable the appropriate compiler flags. Additionally, the `<generator>` header is part of the experimental coroutine support and might be located in a different namespace depending on your compiler and standard library implementation.