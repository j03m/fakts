Futures are  a foundational concept, and understanding them can make working with asynchronous code much easier. Let's break down what futures are and how they work.

### What is a Future?

A future is a programming construct that represents a value that will be available at some point in the future. It's a way to manage the result of an asynchronous operation, allowing you to write code that can start a computation and then continue doing other work while waiting for the result.

Futures are often used in multithreaded programming to synchronize threads and retrieve results from parallel computations.

### How Do Futures Work?

In C++, a `std::future` is a class template that represents a future value. Here's a step-by-step explanation of how you might use a future:

1. **Start an Asynchronous Operation:** You can start an asynchronous operation that returns a `std::future`. This operation might be a computation running on another thread, an I/O operation, etc.

2. **Continue Other Work:** While the asynchronous operation is running, your code can continue doing other work. The future acts as a handle to the result of the operation, but it doesn't block your code from continuing.

3. **Retrieve the Result:** When you need the result of the asynchronous operation, you can call the `get` method on the future. If the operation is not yet complete, `get` will block until the result is available. Once the result is ready, `get` returns it.

### Simple Example with `std::async`

Here's a simple example that uses `std::async` to run a computation on another thread and returns a `std::future`:

```cpp
#include <iostream>
#include <future>
#include <thread>

int compute_sum(int a, int b) {
    std::this_thread::sleep_for(std::chrono::seconds(2)); // Simulate a long computation
    return a + b;
}

int main() {
    // Start the computation on another thread
    std::future<int> future_sum = std::async(std::launch::async, compute_sum, 5, 7);

    // Do other work here...

    // Retrieve the result (this will block if the computation is not yet complete)
    int sum = future_sum.get();
    std::cout << "Sum: " << sum << '\n'; // Output: Sum: 12

    return 0;
}
```

### Key Points

- **Non-blocking:** Futures allow you to write non-blocking code, where you can start a long-running operation and then do other work while waiting for the result.
- **Thread-Safe:** Retrieving the result from a future is thread-safe, so you don't have to worry about synchronizing access to the result.
- **One-time Use:** A `std::future` can only be `get` once. After you've retrieved the result, the future is no longer valid.

Futures are a powerful tool for writing concurrent and parallel code in C++. They provide a way to manage the complexity of asynchronous programming, making it easier to write code that's both efficient and correct. Understanding futures is a key step toward working with more advanced features like C++20 coroutines, as shown in the previous example.


### Downloader

This example demonstrates how to create an asynchronous function that downloads content from a given URL and returns it as a `std::future<std::string>`.

#### Code Example

```cpp
#include <iostream>
#include <string>
#include <future>
#include <coroutine>
#include <curl/curl.h>

size_t write_callback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::future<std::string> download_content(const std::string& url) {
    co_await std::suspend_always{}; // Yield to the caller

    CURL* curl = curl_easy_init();
    std::string response_data;

    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_data);
        CURLcode res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "CURL error: " << curl_easy_strerror(res) << '\n';
        }
        curl_easy_cleanup(curl);
    }

    co_return response_data; // Return the downloaded content
}

int main() {
    auto future_content = download_content("https://www.example.com");
    std::string content = future_content.get();
    std::cout << "Downloaded content:\n" << content << '\n';
    return 0;
}
```

#### Explanation

1. **Coroutine Function `download_content`:** This function takes a URL and returns a `std::future<std::string>` containing the downloaded content. It uses libcurl to perform the HTTP request.

2. **`write_callback`:** This is a callback function used by libcurl to write the downloaded data to a `std::string`.

3. **`co_await std::suspend_always{};`:** This line suspends the coroutine's execution and yields control back to the caller. This ensures that the download operation doesn't block the calling thread.

4. **`co_return`:** This returns the downloaded content to the caller as a `std::future<std::string>`.

5. **Main Function:** The main function calls `download_content`, gets the future, and prints the downloaded content.

This example illustrates how you can use C++20 coroutines to perform asynchronous I/O operations, such as downloading content from the web. By returning a `std::future`, the coroutine allows the caller to retrieve the result when it's ready, without blocking the calling thread.

Note: You'll need to link against libcurl and include its headers to compile this code. Make sure your compiler supports C++20, and you may need to enable the appropriate compiler flags.