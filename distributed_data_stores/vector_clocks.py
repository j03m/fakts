'''
In this enhanced example, the `VectorClock` class now handles key/value pairs of data, in addition to tracking the timestamps for each node.

Here's how it works:

1. **Initialization**: Each node (Alice, Bob, Carol) starts with a timestamp of 0. The `data` dictionary will store the key/value pairs along with the corresponding vector clock at the time of update.

2. **Updating Data**: When a node updates a value, it increments its own timestamp in the vector clock and stores the key/value pair along with a copy of the current vector clock. For example, when Alice updates a value with the key "gossip", her timestamp is incremented, and the value is stored with the current state of her vector clock.

3. **Receiving Messages**: When a node receives a message, it updates its vector clock based on the information in the received message. It takes the maximum of each timestamp in its clock and the clock in the message. Then, it updates its data with the new key/value pair and again increments its own timestamp.

### Output Explanation:

- After Alice updates a value: Alice's timestamp is incremented to 1. The data "gossip" with the value "Alice heard something interesting" is stored along with Alice's current vector clock.

- After Bob receives Alice's update: Bob updates his vector clock by comparing his clock with Alice's. He then updates the data with the "gossip" value received from Alice and increments his timestamp. This ensures that Bob's clock now reflects that he is aware of the latest update from Alice.

This model allows each node to track not only the values but also the context (the state of the system) in which those values were updated or received. This is crucial in distributed systems for resolving conflicts and understanding the causal relationships between different updates.
'''


class VectorClock:
    def __init__(self, nodes):
        self.timestamps = {node: 0 for node in nodes}
        self.data = {}

    def update(self, node, key, value):
        # Update the timestamp for the node
        self.timestamps[node] += 1
        # Update the data with the new key-value pair
        self.data[key] = (value, dict(self.timestamps))

    def receive_message(self, node, message_clock, key, value):
        # Update the vector clock based on the message received
        for key in self.timestamps:
            self.timestamps[key] = max(self.timestamps[key], message_clock[key])
        # Update the data with the new key-value pair
        self.data[key] = (value, dict(self.timestamps))
        # Update the timestamp for the node
        self.update(node, key, value)

    def __str__(self):
        return f"Timestamps: {self.timestamps}, Data: {self.data}"

# Example usage
nodes = ["Alice", "Bob", "Carol"]
vc = VectorClock(nodes)

# Alice updates a value
vc.update("Alice", "gossip", "Alice heard something interesting")
print("After Alice updates a value:", vc)

# Bob receives Alice's update
vc.receive_message("Bob", vc.timestamps, "gossip", "Alice heard something interesting")
print("After Bob receives Alice's update:", vc)

