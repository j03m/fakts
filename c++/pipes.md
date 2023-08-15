### Pipes: Overview

A pipe is a unidirectional communication channel that connects two processes. One process writes to the pipe, and the other reads from it. Pipes can be used for parent-child communication, or between two unrelated processes using named pipes (FIFOs).

### Creating a Pipe

A pipe is created using the `pipe` system call, which takes an array of two file descriptors:

```cpp
int fd[2];
pipe(fd);
```

- `fd[0]`: The file descriptor for reading from the pipe.
- `fd[1]`: The file descriptor for writing to the pipe.

### Non-Trivial Example: Parent-Child Communication

Let's create a non-trivial example where a parent process sends a series of numbers to a child process. The child process calculates the sum and sends it back to the parent.

#### Code

```cpp
#include <iostream>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int parent_to_child[2], child_to_parent[2];

    // Create pipes
    pipe(parent_to_child);
    pipe(child_to_parent);

    pid_t pid = fork();

    if (pid == 0) { // Child process
        close(parent_to_child[1]); // Close unused write end
        close(child_to_parent[0]); // Close unused read end

        int sum = 0, value;
        while (read(parent_to_child[0], &value, sizeof(value)) > 0) {
            sum += value;
        }

        write(child_to_parent[1], &sum, sizeof(sum));

        close(parent_to_child[0]);
        close(child_to_parent[1]);
        exit(0);
    } else { // Parent process
        close(parent_to_child[0]); // Close unused read end
        close(child_to_parent[1]); // Close unused write end

        for (int i = 1; i <= 10; ++i) {
            write(parent_to_child[1], &i, sizeof(i));
        }

        close(parent_to_child[1]); // Close write end to signal EOF to child

        int sum;
        read(child_to_parent[0], &sum, sizeof(sum));
        std::cout << "Sum from child: " << sum << std::endl;

        close(child_to_parent[0]);
        wait(NULL); // Wait for child to terminate
    }

    return 0;
}
```

#### Explanation

1. **Create Two Pipes**: One for parent-to-child communication and one for child-to-parent communication.
2. **Fork**: Create a child process using `fork`.
3. **Parent Process**: Sends numbers 1 to 10 to the child and reads the sum from the child.
4. **Child Process**: Reads numbers from the parent, calculates the sum, and sends it back to the parent.
5. **Close Unused Ends**: Each process must close the ends of the pipes that it's not using. This is important for signaling EOF and avoiding deadlocks.


### Named Pipes

Named pipes, or FIFOs (First In, First Out), are used for communication between unrelated processes. They are created using the mkfifo command or the mkfifo system call.

### Step 1: Create Named Pipes

First, we'll create two named pipes: one for writer-to-reader communication and one for reader-to-writer communication. You can create these named pipes using the `mkfifo` command:

```bash
mkfifo writer_to_reader
mkfifo reader_to_writer
```

### Step 2: Writer Process

The writer process will open the named pipes, send a series of numbers to the reader, and then read the sum from the reader.

```cpp
#include <fcntl.h>
#include <unistd.h>
#include <iostream>

int main() {
    int fd_writer_to_reader = open("writer_to_reader", O_WRONLY);
    int fd_reader_to_writer = open("reader_to_writer", O_RDONLY);

    for (int i = 1; i <= 10; ++i) {
        write(fd_writer_to_reader, &i, sizeof(i));
    }

    int sum;
    read(fd_reader_to_writer, &sum, sizeof(sum));
    std::cout << "Sum from reader: " << sum << std::endl;

    close(fd_writer_to_reader);
    close(fd_reader_to_writer);

    return 0;
}
```

### Step 3: Reader Process

The reader process will open the named pipes, read the numbers from the writer, calculate the sum, and send it back to the writer.

```cpp
#include <fcntl.h>
#include <unistd.h>

int main() {
    int fd_writer_to_reader = open("writer_to_reader", O_RDONLY);
    int fd_reader_to_writer = open("reader_to_writer", O_WRONLY);

    int sum = 0, value;
    for (int i = 0; i < 10; ++i) {
        read(fd_writer_to_reader, &value, sizeof(value));
        sum += value;
    }

    write(fd_reader_to_writer, &sum, sizeof(sum));

    close(fd_writer_to_reader);
    close(fd_reader_to_writer);

    return 0;
}
```

### Choosing

Yes, Joe, one of the significant differences between unnamed (anonymous) pipes and named pipes (FIFOs) is that named pipes need to be precreated and have a presence in the filesystem, while unnamed pipes are created in memory and do not have a filesystem representation. Let's explore the differences and the reasons you might choose one over the other:

### Unnamed (Anonymous) Pipes

- **Creation**: Created in memory using the `pipe` system call.
- **Communication**: Used for communication between related processes, such as parent and child.
- **Lifetime**: Tied to the processes using it; destroyed when all file descriptors referring to the pipe are closed.
- **Visibility**: Does not have a presence in the filesystem; only accessible to the process that created it and its descendants.
- **Use Case**: Ideal for parent-child communication, command-line pipelines, and other scenarios where the communicating processes have a clear parent-child or sibling relationship.

### Named Pipes (FIFOs)

- **Creation**: Created in the filesystem using the `mkfifo` command or system call.
- **Communication**: Can be used for communication between unrelated processes.
- **Lifetime**: Continues to exist in the filesystem until explicitly deleted; can be used by multiple processes over time.
- **Visibility**: Has a name in the filesystem; any process that knows the name can open and use the pipe.
- **Use Case**: Suitable for communication between unrelated processes, complex IPC patterns, or scenarios where the communicating processes may not have a clear parent-child relationship.

### Choosing Between Unnamed and Named Pipes

- **Related Processes**: If you're communicating between a parent and its child or other closely related processes, unnamed pipes are simpler and more efficient.
- **Unrelated Processes**: If you need to communicate between unrelated processes or processes that may not be running at the same time, named pipes provide the flexibility you need.
- **Filesystem Presence**: If you need a pipe that persists beyond the lifetime of the processes using it, or if you need a pipe that can be accessed by name by different processes, a named pipe is the way to go.
- **Performance**: Unnamed pipes are generally more efficient as they are held in memory and don't involve filesystem operations.

### Conclusion

The choice between unnamed and named pipes depends on the specific requirements of your IPC scenario. Unnamed pipes are typically used for simple parent-child communication, while named pipes offer more flexibility for complex or unrelated process communication. Understanding the differences and the use cases for each type of pipe can help you choose the right tool for your IPC needs.