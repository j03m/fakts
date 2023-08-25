The CAP theorem is a fundamental concept in distributed computing and is often considered when designing a distributed database system. Let's explore the three properties (Consistency, Availability, and Partition Tolerance) and the combinations of two that can exist in real-world systems.

### 1. Consistency and Availability (CA)

In this combination, the system prioritizes maintaining data consistency and availability but doesn't handle network partitions well.

#### Example: Traditional Relational Databases
A typical relational database like MySQL or PostgreSQL running on a single node or a tightly coupled cluster might fall into this category. It ensures that all read and write operations are consistent and available, but if the network between nodes gets partitioned, the system may not function properly.

### 2. Consistency and Partition Tolerance (CP)

In this combination, the system emphasizes maintaining data consistency and can handle network partitions but may sacrifice availability.

#### Example: HBase
HBase, a distributed database, is often considered a CP system. It ensures that reads and writes are consistent across the cluster, and it can handle network partitions. However, if too many nodes fail, the system might become unavailable for some operations.

### 3. Availability and Partition Tolerance (AP)

This combination prioritizes availability and partition tolerance, even if it means that the data might be temporarily inconsistent across nodes.

#### Example: Apache Cassandra
Apache Cassandra is designed to provide high availability and partition tolerance. If a network partition occurs, or some nodes are down, the system continues to operate, possibly providing stale or inconsistent data. Eventually, the system will reconcile the data using mechanisms like eventual consistency.

## Businesses

Let's look at real-world business cases where each combination of CAP properties would be essential and why.

### 1. Consistency and Availability (CA)

#### Business Case: Banking Systems
- **Why Consistency?** In a banking system, it's crucial that all transactions are recorded accurately and consistently. If two clients simultaneously access an account, they must both see the exact same balance. Otherwise, this could lead to errors like double-spending.
- **Why Availability?** Banking services must be available at all times to handle customer transactions. A failure in availability might lead to significant customer dissatisfaction and potential financial loss.

### 2. Consistency and Partition Tolerance (CP)

#### Business Case: Medical Record Systems
- **Why Consistency?** In healthcare, it's vital to have consistent medical records. If different healthcare providers see different data for the same patient, it could lead to incorrect diagnoses or treatments.
- **Why Partition Tolerance?** Healthcare providers might be spread across various locations, and network partitions can happen. The system must continue to function even if some parts of the network are unreachable, ensuring that localized issues don't affect the entire system.

### 3. Availability and Partition Tolerance (AP)

#### Business Case: E-Commerce Platforms
- **Why Availability?** An e-commerce site must always be available to handle customer requests. If the site goes down, even temporarily, it can lead to a significant loss of sales and customer trust.
- **Why Partition Tolerance?** E-commerce platforms often operate globally, with distributed data centers. Network partitions between these data centers must not bring down the entire system. Some temporary inconsistency (like showing an outdated inventory count) might be acceptable, as long as the system is available and eventually reconciles the data.

### Summary

- **Banking Systems (CA):** Need consistency to prevent errors like double-spending, and availability to ensure uninterrupted service.
- **Medical Record Systems (CP):** Require consistency for accurate medical care and partition tolerance to handle network issues between various healthcare locations.
- **E-Commerce Platforms (AP):** Prioritize availability to maintain sales and customer experience, and partition tolerance to handle global distribution and network failures, even if it means temporary inconsistency.

The choice between these combinations depends on the specific requirements and trade-offs of the business case. Understanding the CAP theorem helps businesses and engineers to design systems that align with organizational goals and customer needs. In practice, achieving a perfect balance between these properties is complex, and systems may be tuned to favor one property over the others based on changing demands and conditions.

## Modeling with Consistent Hashing

### Consistent Hashing

Consistent hashing is a method used to distribute data across multiple servers. It ensures that when a server is added or removed from the system, only a minimal amount of data needs to be reorganized. This is in contrast to traditional methods, where adding or removing a server can cause a significant amount of data to be moved around.

### Hash Ring

In consistent hashing, the servers and keys are mapped onto a logical ring called the "hash ring." The ring is typically represented as a 0 to \(2^n - 1\) range, where \(n\) is the number of bits in the hash value. When a server is added, it's placed at a position on the ring based on its hash value. When a key (data) needs to be stored, its hash value determines the position on the ring, and then the data is stored on the server that's closest to that position in the clockwise direction.

### Replication

Replication is done by storing copies of the data on the first \(N\) servers encountered in the clockwise direction from the key's position. If \(N = 3\), then three servers will have copies of the data. This ensures high availability and fault tolerance. If one server goes down, the data is still accessible from the other replicas.

### Example with 10 Servers

Now, let's consider your the scenario with 10 servers and explain how the data could be replicated.

1. **Hash Ring Creation**: Let's assume you have 10 servers (s0 to s9), and they are placed on the hash ring based on their hash values.
2. **Key Mapping**: Suppose a key (key0) is mapped to the position corresponding to server s1 on the ring.
3. **Replication**: If \(N = 3\), the key will be replicated on s1 and the next two servers in the clockwise direction. If the servers are placed in such a way that s1 is followed by s9 and s0, then yes, the data would be replicated on s1, s9, and s0.

Here's a simple illustration:

```plaintext
        s3
     /       \
s4           s2
    \        /
        s1
    /        \
s5           s9
     \       /
        s0
    /        \
s6           s8
     \       /
        s7
```

If key0 is mapped to s1, and \(N = 3\), then the replicas would be on s1, s9, and s0.

### 1. Data Replication

#### How it Works
- **Hash Ring**: Servers are arranged in a ring based on their hash values.
- **Replication**: When a key is mapped to a position on the ring, it's replicated over \( N \) servers, walking clockwise from that position.
- **Virtual Nodes**: Sometimes, virtual nodes are used to ensure an even distribution, and unique physical servers are chosen to avoid redundancy.
- **Multi-Data Center**: For higher reliability, replicas are placed across different data centers.

#### Illustration
Consider 5 servers (s0 to s4) and a key (key0) mapped to s1 with \( N = 3 \).

```plaintext
        s2
     /       \
s3           s1 (key0)
    \        /
        s0
    /        \
s4           -
     \       /
        -
```

Here, key0 is replicated at s1, s2, and s3.

### 2. Quorum Consensus

#### Definitions
- **N**: Number of replicas (e.g., \( N = 3 \))
- **W**: Write quorum, the number of acknowledgments needed for a write to be successful (e.g., \( W = 1 \))
- **R**: Read quorum, the number of responses needed for a read to be successful

#### How it Works
- **Write Operation**: A write must be acknowledged by at least \( W \) replicas to be successful.
- **Read Operation**: A read must wait for responses from at least \( R \) replicas to be successful.
- **Tradeoff**: Lower \( W \) or \( R \) means quicker responses but less consistency. Higher values mean better consistency but slower queries.

#### Illustration
Consider \( N = 3 \), \( W = 1 \), and the same key0 replicated at s0, s1, and s2.

- **Write**: When writing key0, only one acknowledgment (e.g., from s1) is needed for success.
- **Read**: Depending on the value of \( R \), you may need one or more responses for a successful read.

```plaintext
Write to key0 (W = 1)
        s2
     /       \
s3          s1 (ack)
    \        /
        s0
    /        \
s4           -
     \       /
        -
```

Here, only acknowledgment from s1 is needed for the write to be considered successful.

### 3. Consistency and Latency

- **W or R = 1**: Faster operations but potentially less consistency.
- **W or R > 1**: Better consistency, but slower operations (waiting for more replicas).

### Conclusion

The given text describes a complex mechanism for ensuring data availability and consistency in a distributed system:

- **Data Replication**: Keys are replicated over \( N \) servers, potentially across data centers.
- **Quorum Consensus**: Write and read operations need acknowledgments/responses from \( W \) or \( R \) replicas, respectively.
- **Consistency Tradeoff**: The configuration of \( W \), \( R \), and \( N \) balances latency and consistency.

### Strong vs Eventually Consistent

1. **Fast Read (R = 1, W = N)**:
   - **Read**: Since \( R = 1 \), only one acknowledgment from a replica is needed for a read to be successful. This leads to fast read operations.
   - **Write**: Since \( W = N \), all replicas must acknowledge a write, ensuring that all replicas have the data, but making writes slower.

2. **Fast Write (W = 1, R = N)**:
   - **Write**: Since \( W = 1 \), only one acknowledgment from a replica is needed for a write to be successful. This leads to fast write operations.
   - **Read**: Since \( R = N \), all replicas must respond to a read, ensuring that the most consistent data is read, but making reads slower.

3. **Strong Consistency (W + R > N)**:
   - If the sum of the write and read quorums is greater than the number of replicas, it ensures that there is always an overlap between the replicas written to and read from. This guarantees strong consistency.
   - **Common Configuration**: \( N = 3, W = R = 2 \) is a typical setup to achieve strong consistency.

4. **Weak Consistency (W + R \leq N)**:
   - If the sum of the write and read quorums is less than or equal to the number of replicas, there might be scenarios where writes are acknowledged by some replicas and reads are performed from others. This can lead to weak or eventual consistency.

### Illustration

Consider \( N = 3 \):

- **Fast Read**: \( R = 1, W = 3 \)
- **Fast Write**: \( W = 1, R = 3 \)
- **Strong Consistency**: \( W = 2, R = 2 \) (or any configuration where \( W + R > 3 \))

### Conclusion

The relationship between \( W \), \( R \), and \( N \) defines the trade-offs between read and write latency and the level of consistency in a distributed system. By tuning these parameters, different levels of performance and consistency can be achieved, depending on the specific requirements of the application. Systems like Apache Cassandra allow you to configure these parameters to tailor the database's behavior to your needs.


## Random: Hash ring with just dedicated Backups?

I started this part up because when I worked in internet games at scale we didn't use consistent hashing.
We used a normal hash on uuid hash(uuid) % num_servers to pick a shard and then had a dedicated backup
for each shard. If a shard went down we had an agent to promote the backup. Unfortunately, if the backup went 
down we were dead. :( However, I did a thought exercise on what consistent hashing would look like with dedicated backups

### Combining Consistent Hashing with Dedicated Backups

1. **Consistent Hashing**: Use consistent hashing to distribute keys across a set of servers on a hash ring. This ensures that adding or removing servers only affects a minimal portion of the data.
2. **Dedicated Backups**: For each server \( X \), assign a specific backup server \( X' \). Data on server \( X \) is replicated only to its corresponding backup \( X' \).

### Advantages

- **Simplicity in Replication**: By having exactly one backup for each server, the replication logic is simplified.
- **Fault Tolerance**: If a server fails, its designated backup can take over, ensuring availability.
- **Scalability**: Using consistent hashing helps in scaling the system, as adding or removing servers minimizes data movement.

### Potential Challenges

- **Backup Server Selection**: Choosing an appropriate backup for each server can be non-trivial. If backups are not distributed evenly, some servers might become hotspots.
- **Recovery from Multiple Failures**: If both a server and its dedicated backup fail simultaneously, data loss can occur. In a system where each key is replicated across \( N \) servers, there might be more resilience to simultaneous failures.
