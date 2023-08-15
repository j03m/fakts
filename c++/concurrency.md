### 6. **Concurrency**

Concurrency refers to the ability of a system to perform multiple tasks simultaneously. In C++, this is achieved through various constructs and libraries that allow for multithreading and synchronization.

#### a. **Threads and the `std::thread` Class**

Threads are the smallest unit of a CPU's execution and can run concurrently with other threads. In C++, the `std::thread` class provides a way to create and manage threads.

**Example: Creating a Thread**

```cpp
#include <iostream>
#include <thread>

void print_hello() {
    std::cout << "Hello from thread!\n";
}

int main() {
    std::thread t(print_hello);
    t.join(); // Wait for the thread to finish
    return 0;
}
```

#### b. **Mutexes, Locks, and the `std::mutex` Class**

Mutexes (short for "mutual exclusion") are used to prevent multiple threads from simultaneously executing critical sections of code that access shared resources.

**Example: Using a Mutex to Protect Shared Data**

```cpp
#include <iostream>
#include <thread>
#include <mutex>

std::mutex mtx;

void print_with_lock(int id) {
    std::lock_guard<std::mutex> lock(mtx);
    std::cout << "Thread " << id << " is running\n";
}

int main() {
    std::thread t1(print_with_lock, 1);
    std::thread t2(print_with_lock, 2);
    t1.join();
    t2.join();
    return 0;
}
```

#### c. **Condition Variables**

Condition variables are synchronization primitives used to block threads until notified to proceed. They are often used in conjunction with a mutex to safely wait for a condition to be met.

**Example: Using a Condition Variable**

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>

std::mutex mtx;
std::condition_variable cv;
bool ready = false;

void wait_for_signal() {
    std::unique_lock<std::mutex> lock(mtx);
    cv.wait(lock, [] { return ready; });
    std::cout << "Thread is now running\n";
}

int main() {
    std::thread t(wait_for_signal);
    std::this_thread::sleep_for(std::chrono::seconds(1)); // Simulate some work
    {
        std::lock_guard<std::mutex> lock(mtx);
        ready = true;
    }
    cv.notify_one(); // Notify the waiting thread
    t.join();
    return 0;
}
```

Here's another example that might help illustrate the concept more clearly:

### Producer-Consumer Problem

Imagine you have two types of threads: producers and consumers. Producers generate data and put it into a shared buffer, while consumers take data out of the buffer and process it. If the buffer is empty, consumers must wait until there is data to consume. If the buffer is full, producers must wait until there is space to produce more data.

A condition variable can be used to synchronize the producers and consumers, ensuring that they wait and proceed at the appropriate times.

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>

std::mutex mtx;
std::condition_variable cv_producer, cv_consumer;
std::queue<int> buffer;
const int buffer_size = 5;

void producer(int id) {
    for (int i = 0; i < 10; ++i) {
        std::unique_lock<std::mutex> lock(mtx);
        cv_producer.wait(lock, [] { return buffer.size() < buffer_size; });
        buffer.push(i);
        std::cout << "Producer " << id << " produced " << i << '\n';
        lock.unlock();
        cv_consumer.notify_one(); // Notify a waiting consumer
    }
}

void consumer(int id) {
    for (int i = 0; i < 10; ++i) {
        std::unique_lock<std::mutex> lock(mtx);
        cv_consumer.wait(lock, [] { return !buffer.empty(); });
        int value = buffer.front();
        buffer.pop();
        std::cout << "Consumer " << id << " consumed " << value << '\n';
        lock.unlock();
        cv_producer.notify_one(); // Notify a waiting producer
    }
}

int main() {
    std::thread p1(producer, 1);
    std::thread c1(consumer, 1);
    p1.join();
    c1.join();
    return 0;
}
```

In this example:

- Producers wait on `cv_producer` if the buffer is full.
- Consumers wait on `cv_consumer` if the buffer is empty.
- When a producer adds an item to the buffer, it notifies a waiting consumer.
- When a consumer removes an item from the buffer, it notifies a waiting producer.

The use of condition variables ensures that the producers and consumers wait and proceed in a coordinated manner, avoiding issues like overfilling the buffer or trying to consume from an empty buffer.

This example illustrates how condition variables can be used to synchronize threads in a way that is both efficient (threads are not busy-waiting) and safe (the mutex ensures that the shared buffer is accessed by only one thread at a time).

#### d. **Atomic Operations and the `std::atomic` Class**

Atomic operations are operations that complete in a single step without being interrupted. The `std::atomic` class template provides a way to represent atomic types, which support lock-free, thread-safe operations.

**Example: Using an Atomic Variable**

```cpp
#include <iostream>
#include <thread>
#include <atomic>

std::atomic<int> counter(0);

void increment() {
    for (int i = 0; i < 1000; ++i) {
        ++counter;
    }
}

int main() {
    std::thread t1(increment);
    std::thread t2(increment);
    t1.join();
    t2.join();
    std::cout << "Counter: " << counter.load() << '\n'; // Output: Counter: 2000
    return 0;
}
```

### 1. **Counting Semaphores (`std::counting_semaphore`)**

A counting semaphore can control access to a resource with multiple identical instances. It's useful in scenarios like managing a pool of identical resources, such as database connections.

**Example: Managing a Pool of Workers**

```cpp
#include <iostream>
#include <thread>
#include <semaphore>

std::counting_semaphore<5> semaphore; // 5 available resources

void worker(int id) {
    semaphore.acquire();
    std::cout << "Worker " << id << " is working\n";
    std::this_thread::sleep_for(std::chrono::seconds(1));
    semaphore.release();
}

int main() {
    std::thread workers[10];
    for (int i = 0; i < 10; ++i) {
        workers[i] = std::thread(worker, i);
    }
    for (int i = 0; i < 10; ++i) {
        workers[i].join();
    }
    return 0;
}
```

### 2. **Timed Mutexes (`std::timed_mutex`)**

Timed mutexes allow threads to attempt to acquire a lock for a specified time. They can be used in scenarios where a thread should not wait indefinitely for a resource, such as in real-time systems.

**Example: Trying to Lock a Resource for a Limited Time**

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>

std::timed_mutex timed_mtx;

void try_locking(int id) {
    if (timed_mtx.try_lock_for(std::chrono::seconds(1))) {
        std::cout << "Thread " << id << " acquired the lock\n";
        std::this_thread::sleep_for(std::chrono::seconds(2));
        timed_mtx.unlock();
    } else {
        std::cout << "Thread " << id << " failed to acquire the lock\n";
    }
}

int main() {
    std::thread t1(try_locking, 1);
    std::thread t2(try_locking, 2);
    t1.join();
    t2.join();
    return 0;
}
```

### 3. **Shared Timed Mutexes (`std::shared_timed_mutex`)**

Shared timed mutexes allow multiple readers but only one writer. They are useful in scenarios like caching systems, where many threads may read a value, but only one should update it.

**Example: Multiple Readers, Single Writer**

```cpp
#include <iostream>
#include <thread>
#include <shared_mutex>

std::shared_timed_mutex shared_mtx;

void read_data(int id) {
    shared_mtx.lock_shared();
    std::cout << "Thread " << id << " is reading\n";
    shared_mtx.unlock_shared();
}

void write_data() {
    shared_mtx.lock();
    std::cout << "Writing data\n";
    shared_mtx.unlock();
}

int main() {
    std::thread t1(read_data, 1);
    std::thread t2(read_data, 2);
    std::thread t3(write_data);
    t1.join();
    t2.join();
    t3.join();
    return 0;
}
```

### 4. **Barriers (`std::barrier`)**

Barriers synchronize multiple threads, making them wait until all have reached a particular point. They are useful in parallel algorithms where threads must synchronize at certain stages, such as in parallel matrix multiplication.

**Example: Synchronizing Threads at a Barrier**

```cpp
#include <iostream>
#include <thread>
#include <barrier>

std::barrier sync_point(3); // 3 threads must reach the barrier

void synchronized_task(int id) {
    std::cout << "Thread " << id << " before barrier\n";
    sync_point.arrive_and_wait();
    std::cout << "Thread " << id << " after barrier\n";
}

int main() {
    std::thread t1(synchronized_task, 1);
    std::thread t2(synchronized_task, 2);
    std::thread t3(synchronized_task, 3);
    t1.join();
    t2.join();
    t3.join();
    return 0;
}
```

### 5. **Latches (`std::latch`)**

Latches allow one or more threads to wait until a specified number of events have occurred. They can be used in scenarios like initializing shared resources before allowing worker threads to proceed.

**Example: Waiting for Initialization**

```cpp
#include <iostream>
#include <thread>
#include <latch>

std::latch start_gate(3); // 3 threads must count down

void wait_for_start(int id) {
    std::cout << "Thread " << id << " waiting\n";
    start_gate.wait();
    std::cout << "Thread " << id << " started\n";
}

int main() {
    std::thread t1(wait_for_start, 1);
    std::thread t2(wait_for_start, 2);
    std
    .this_thread::sleep_for(std::chrono::seconds(1));
    start_gate.count_down(3); // Allow all threads to start
    t1.join();
    t2.join();
    t3.join();
    return 0;
}
```


