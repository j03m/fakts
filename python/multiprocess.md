### Multiprocessing in Python

Lets us get around the GIL (see threading)

#### a. **Introduction**
The `multiprocessing` module in Python provides support for parallelizing your code by running multiple processes concurrently. Each process has its own Python interpreter and memory space, which avoids conflicts but also makes sharing data more complex.

#### b. **Critical Sections and Locks**
Just like with threading, you may need to synchronize access to shared resources in multiprocessing. You can use a `multiprocessing.Lock` to protect critical sections.

##### **Example: Using Locks**
```python
from multiprocessing import Process, Lock, Value
import time

def increment_counter(counter, lock):
    with lock:
        temp = counter.value
        time.sleep(0.1)  # Simulate some computation
        counter.value = temp + 1

counter = Value('i', 0)
lock = Lock()
processes = [Process(target=increment_counter, args=(counter, lock)) for _ in range(10)]

for process in processes:
    process.start()
for process in processes:
    process.join()

print(counter.value)  # Output: 10
```

#### c. **Variable Access and Shared Memory**
Since processes don't share memory space, you'll need to use special shared objects if you want to share data between processes. You can use `Value` or `Array` from the `multiprocessing` module.

##### **Example: Shared Memory**
```python
from multiprocessing import Process, Value

def add_to_value(shared_value, amount):
    shared_value.value += amount

shared_value = Value('d', 0.0)
process = Process(target=add_to_value, args=(shared_value, 3.14))
process.start()
process.join()

print(shared_value.value)  # Output: 3.14
```

#### d. **Communication Between Processes**
You can use `Queue` or `Pipe` from the `multiprocessing` module to facilitate communication between processes.

##### **Example: Using Queue**
```python
from multiprocessing import Process, Queue

def square_numbers(numbers, queue):
    for number in numbers:
        queue.put(number * number)

numbers = [1, 2, 3, 4]
queue = Queue()
process = Process(target=square_numbers, args=(numbers, queue))
process.start()
process.join()

squares = [queue.get() for _ in numbers]
print(squares)  # Output: [1, 4, 9, 16]
```

### a. **Pools**
A pool is a collection of worker processes that can execute tasks in parallel. The `Pool` class provides a convenient way to parallelize the execution of a function across multiple input values.

#### **Example: Using Pool**
```python
from multiprocessing import Pool

def square(x):
    return x * x

with Pool(5) as p:  # Create a pool with 5 worker processes
    result = p.map(square, [1, 2, 3, 4, 5])
    print(result)  # Output: [1, 4, 9, 16, 25]
```

- `Pool.map()`: Maps input values to the target function and collects the results.
- `Pool.apply_async()`: Applies a function asynchronously and returns a result object.

### c. **Contexts**
Contexts provide a way to select the start method used to create child processes. Different start methods have different characteristics and are suitable for different environments.

- **`spawn`**: The default on Windows. It starts a fresh Python interpreter process, so the code must be importable by the child.
- **`fork`**: The default on Unix. It forks the Python interpreter, so the child process is identical to the parent at the time of the fork.
- **`forkserver`**: Similar to `fork`, but it uses a server process to create child processes.

#### **Example: Using Context**
```python
from multiprocessing import get_context

def print_hello():
    print('Hello, World!')

if __name__ == '__main__':
    ctx = get_context('spawn')  # Use the 'spawn' start method
    process = ctx.Process(target=print_hello)
    process.start()
    process.join()
```


### a. **What is a Manager?**
A `Manager` object controls a server process that holds Python objects and allows other processes to manipulate them. It provides a way to create shared objects that can be accessed across different processes.

### b. **Types of Managers**
There are several types of managers, including:

- `Manager()`: A general-purpose manager that provides a variety of shared objects.
- `Value()`, `Array()`: Specialized managers for sharing variables and arrays.

### c. **Using a Manager**

#### **Example: Shared Dictionary**
```python
from multiprocessing import Manager, Process

def update_dict(shared_dict):
    shared_dict['count'] += 1

if __name__ == '__main__':
    manager = Manager()
    shared_dict = manager.dict({'count': 0})

    processes = [Process(target=update_dict, args=(shared_dict,)) for _ in range(10)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()

    print(shared_dict['count'])  # Output: 10
```

#### **Example: Shared List**
```python
from multiprocessing import Manager, Process

def append_to_list(shared_list, value):
    shared_list.append(value)

if __name__ == '__main__':
    manager = Manager()
    shared_list = manager.list()

    processes = [Process(target=append_to_list, args=(shared_list, i)) for i in range(5)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()

    print(shared_list)  # Output: [0, 1, 2, 3, 4]
```

### d. **Synchronization**
Manager objects include synchronization operations, so you don't need to worry about multiple processes accessing them simultaneously. However, complex operations may still require explicit locks.

### Conclusion
The `Manager` class in the `multiprocessing` module provides a way to create shared objects that can be accessed and manipulated by multiple processes. It supports various data types, including dictionaries, lists, namespaces, and more.

Using a `Manager` allows you to share data across processes without worrying about synchronization for simple operations. It's a powerful tool for parallel programming, enabling more complex interactions between processes and facilitating the development of robust and efficient parallel applications.