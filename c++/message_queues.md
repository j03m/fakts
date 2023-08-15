### Message Queues Overview

Message queues are a way to send and receive messages between processes. Unlike pipes, which send a stream of bytes, message queues send discrete messages, each with a specific type. This allows for more complex and organized communication.

### Key Concepts

- **Creation**: Message queues are created using a key, which can be generated using functions like `ftok`.
- **Sending and Receiving**: Processes can send messages to the queue with a specified type, and they can receive messages of a specific type or any type.
- **Ordering**: Messages can be retrieved in the order they were sent, or based on their type.
- **Persistence**: Message queues persist beyond the lifetime of the creating process, unless explicitly deleted.

### Code Example

Let's create two programs: a sender that sends messages to the queue, and a receiver that reads messages from the queue.

#### Sender Program

```c
#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>

struct msg_buffer {
    long msg_type;
    char text[100];
};

int main() {
    key_t key;
    int msg_id;
    struct msg_buffer message;

    key = ftok("progfile", 65);
    msg_id = msgget(key, 0666 | IPC_CREAT);
    message.msg_type = 1;

    printf("Enter text: ");
    fgets(message.text, sizeof(message.text), stdin);

    msgsnd(msg_id, &message, sizeof(message), 0);

    printf("Message sent: %s", message.text);

    return 0;
}
```

#### Receiver Program

```c
#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>

struct msg_buffer {
    long msg_type;
    char text[100];
};

int main() {
    key_t key;
    int msg_id;
    struct msg_buffer message;

    key = ftok("progfile", 65);
    msg_id = msgget(key, 0666 | IPC_CREAT);

    msgrcv(msg_id, &message, sizeof(message), 1, 0);

    printf("Received message: %s", message.text);

    return 0;
}
```

### Usage

1. Compile both programs.
2. Run the receiver program. It will wait for a message.
3. Run the sender program and enter a message. The receiver will print the received message.

### Conclusion

Message queues provide a structured way to send and receive messages between processes. They allow for more complex communication patterns, such as prioritizing messages by type or ensuring that messages are processed in a specific order. Message queues are a powerful tool for IPC and are used in various applications, from simple client-server communication to complex distributed systems.