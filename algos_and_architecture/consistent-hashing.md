### 1. What is Consistent Hashing?
Consistent hashing is a method used to distribute data across multiple nodes (e.g., servers) in a way that minimizes rehashing when a node is added or removed. This is particularly important in distributed systems, such as caching or data storage.

Imagine a ring (called a hash ring) where each point on the ring corresponds to a hash value. The hash values are generated using a hash function like MD5 or SHA-1. The nodes are placed on the ring based on their hash value, and data keys are also mapped to the ring using the same hash function.

#### Real-World Example:
Imagine a distributed cache system like Memcached. Without consistent hashing, adding or removing a server would require rehashing most keys, leading to cache misses and degraded performance. Consistent hashing minimizes this problem.

### 2. Problem: Uneven Distribution
The naive implementation results in the natural hash of a server leading to an uneven distribution of keys. Some servers might get more keys, while others might get fewer. This imbalance can result in uneven load across servers.

### 3. Virtual Nodes to the Rescue
Virtual nodes are a solution to this problem. Instead of placing each physical server once on the ring, we place it multiple times using different hash values. These multiple placements are called virtual nodes. By using virtual nodes, we can ensure a more even distribution of keys.


Implementing consistent hashing with virtual nodes for sharding across multiple Redis servers is an exciting project. Let's start by setting up the initial ring with virtual nodes for 5 Redis servers.

### Step 1: Setting Up the Initial Ring with Virtual Nodes

We'll create a class to handle consistent hashing. The class will include methods for adding a node and finding the appropriate node for a given key. We'll use the `hashlib` library to generate hash values.

Here's the initial code:

```python
import hashlib

class ConsistentHashing:
    def __init__(self, nodes=None, replicas=100):
        self.replicas = replicas
        self.ring = {}
        self.sorted_hashes = []
        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node):
        for i in range(self.replicas):
            virtual_node = f'{node}:{i}'
            hash_value = self.hash(virtual_node)
            self.ring[hash_value] = node
            self.sorted_hashes.append(hash_value)
        self.sorted_hashes.sort()

    def hash(self, key):
        return int(hashlib.sha1(key.encode('utf-8')).hexdigest(), 16)
    
    def get_node(self, key):
        key_hash = self.hash(key)
        idx = self._find_position(key_hash)
        return self.ring[self.sorted_hashes[idx]]

    # note, this is naive and slow, we'll replace it shortly
    def _find_position(self, key_hash):
        for i, node_hash in enumerate(self.sorted_hashes):
            if key_hash <= node_hash:
                return i
        return 0  # Wrap around to the beginning if no suitable node is found

    
# Define the 5 Redis servers
redis_servers = [
    'redis_server_1',
    'redis_server_2',
    'redis_server_3',
    'redis_server_4',
    'redis_server_5',
]

# Create the consistent hashing object
ch = ConsistentHashing(nodes=redis_servers)

# The ring is now set up with virtual nodes for the 5 Redis servers
```

In this code, we have:

- A constructor that initializes the ring and accepts an optional list of nodes.
- A `add_node` method that adds a node and its corresponding virtual nodes to the ring.
- A `hash` method that generates a hash value for a given key using SHA-1.
- In the `_find_position` method, we loop through the sorted hashes (virtual nodes).
- If the key's hash is less than or equal to the hash of a virtual node, we return the index of that virtual node.
- If no suitable virtual node is found (i.e., the key's hash is greater than all virtual nodes' hashes), we return `0` to wrap around to the beginning of the ring.

We've set up the ring with 100 virtual nodes for each physical Redis server. You can adjust the number of replicas (virtual nodes) based on your specific needs.

### Faster searching

We shouldn't blindly loop through the list of hashes. We can be more efficient with a binary search:

```python
def _find_position(self, key_hash):
    left, right = 0, len(self.sorted_hashes) - 1

    while left <= right:
        middle = (left + right) // 2
        middle_hash = self.sorted_hashes[middle]

        if key_hash < middle_hash:
            right = middle - 1
        else:
            left = middle + 1

    return left if left < len(self.sorted_hashes) else 0  # Return the appropriate index, wrap around if needed
```

This is slightly different from a classic binary search because we're not trying to find a match. We just want to round 
into the correct portion of the ring. We want the first value that is greater than our hash or 0 if no such exists.

Let's illustrate the steps taken by our manually implemented binary search algorithm when searching for the key 5 in a ring with hashes `[2, 4, 6, 8, 10]`.

##### Initialization
- `left = 0`
- `right = 4` (length of sorted_hashes minus one)
- `key_hash = 5` (the value we're searching for)

#####  Iteration 1
- `middle = (0 + 4) // 2 = 2` (index of the value 6 in the list)
- `middle_hash = 6`
- Since `key_hash < middle_hash`, we update `right = middle - 1 = 1`

#####  Iteration 2
- `middle = (0 + 1) // 2 = 0` (index of the value 2 in the list)
- `middle_hash = 2`
- Since `key_hash > middle_hash`, we update `left = middle + 1 = 1`

#####  Iteration 3
- `middle = (1 + 1) // 2 = 1` (index of the value 4 in the list)
- `middle_hash = 4`
- Since `key_hash > middle_hash`, we update `left = middle + 1 = 2`

##### Exit the Loop
- Now `left = 2` and `right = 1`, so `left > right`, and we exit the loop.

##### Result
- We return `left = 2`, which is the index of the first virtual node whose hash is greater than or equal to the key's hash (in this case, the hash value 6).

An astute python coder probably knows this is the same functionality as `bisect_left` which
is probably more optimized and better tested than our search:

```python
from bisect import bisect_left

def _find_position(self, key_hash):
    position = bisect_left(self.sorted_hashes, key_hash)
    return position if position < len(self.sorted_hashes) else 0
```


