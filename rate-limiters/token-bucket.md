### Token Bucket Algorithm

Before diving into the code, let's briefly explain the token bucket algorithm.

A token bucket is a simple algorithm used to control the rate of events, such as requests to a server. The bucket has a fixed capacity and tokens are added at a fixed rate. When a request comes in, a token is removed from the bucket. If there are no tokens left, the request is denied.

### Concepts

- **UUID**: A universally unique identifier (UUID) is a 128-bit number used to identify information in computer systems. In this case, we will shard the caching layer by UUID, meaning that each user or resource identified by a UUID will have a separate token bucket.
- **Redis**: Redis is an in-memory key-value database that is often used as a caching layer.
- **Sharding**: Sharding is the practice of splitting a database into smaller, more manageable parts, called shards. In this case, we will use the UUID to determine which shard to use.

### Shard Mapping

First, you'll need a way to map a UUID to a specific Redis shard. A common approach is to use a consistent hashing algorithm. You could hash the UUID and then use the hash value to determine the appropriate shard.

### Multiple Redis Connections

You'll need to manage connections to multiple Redis instances. You might have a list or dictionary of connections, each corresponding to a different shard.

Here's a simple example of how you might implement this:

#### Define the Shards

Define the connections to your different Redis instances. You could configure these based on your actual sharding strategy.

```python
SHARDS = [
    redis.StrictRedis(host='shard1_host', port=6379, db=0),
    redis.StrictRedis(host='shard2_host', port=6379, db=0),
    # Add more shards as needed
]
```

#### Hash Function to Determine Shard

You can use a hash function to determine the appropriate shard for a given UUID. In a real-world scenario, you'd likely use a more sophisticated consistent hashing algorithm.

```python
# notably there is a from redis import RedisCluster
# that may do this for us, but for illustration purposes
def get_shard(uuid):
    shard_index = hash(uuid) % len(SHARDS)
    return SHARDS[shard_index]
```


#### Configuration

First, we'll need to configure the token bucket parameters and connect to the Redis instance.

```python
import redis

# Token bucket parameters
TOKENS_PER_BUCKET = 10
TOKENS_REFILL_RATE = 1  # tokens per second

```

#### 2. Keys

Since we are sharding by UUID, we will create a function that takes a UUID and returns the shard (Redis key) corresponding to that UUID.

```python
def get_shard_key(uuid):
    return f'token_bucket:{uuid}'
```

#### 3. Token Bucket Logic

We'll need functions to add tokens to the bucket and to check whether a request can be handled.

```python
import time

def refill_tokens(uuid):
    redis_conn = get_shard(uuid)
    shard_key = get_shard_key(uuid)
    
    timestamp = time.time()
    redis_conn.set(f'{shard_key}:timestamp', timestamp)

    # Calculate tokens to refill
    last_timestamp = float(redis_conn.get(f'{shard_key}:timestamp') or 0)
    tokens_to_add = (timestamp - last_timestamp) * TOKENS_REFILL_RATE
    current_tokens = float(redis_conn.get(shard_key) or 0)
    new_tokens = min(current_tokens + tokens_to_add, TOKENS_PER_BUCKET)

    # Update the token count
    redis_conn.set(shard_key, new_tokens)

def can_consume_token(uuid):
    shard_key = get_shard_key(uuid)
    redis_conn = get_shard(uuid)
    current_tokens = float(redis_conn.get(shard_key) or 0)

    if current_tokens < 1:
        return False

    # Consume a token
    redis_conn.set(shard_key, current_tokens - 1)
    return True
```

#### 4. Handling Requests

Finally, you can use these functions to handle incoming requests. You would typically integrate this logic into your web server's request handling code.

```python
def handle_request(uuid):
    refill_tokens(uuid)
    if can_consume_token(uuid):
        # Process the request
        pass
    else:
        # Reject the request, e.g., return a 429 'Too Many Requests' response
        pass
```

#### Optimizing

That implementation makes many round trips to redis. We can do better for sure.

```python
def refill_and_consume_token(uuid):
    shard_key = get_shard_key(uuid)
    timestamp = time.time()

    # Use a Redis pipeline to combine operations
    pipe = redis_conn.pipeline()
    pipe.hgetall(shard_key)  # Get the existing values
    pipe.execute()

    # Extract values and calculate new tokens
    last_timestamp, current_tokens = pipe[0]['timestamp'], pipe[0]['tokens']
    tokens_to_add = (timestamp - float(last_timestamp)) * TOKENS_REFILL_RATE
    new_tokens = min(float(current_tokens) + tokens_to_add, TOKENS_PER_BUCKET)

    # Check if a token can be consumed
    if new_tokens < 1:
        return False

    # Update the token count and timestamp in one batch
    pipe.hset(shard_key, 'timestamp', timestamp)
    pipe.hset(shard_key, 'tokens', new_tokens - 1)
    pipe.execute()

    return True
```

```python
def handle_request(uuid):
   if refill_and_consume_token(uuid):
        # Process the request
        pass
    else:
        # Reject the request, e.g., return a 429 'Too Many Requests' response
        pass
```

#### Testability

The current version is pinned to redis and isn't easily unit tested without mocks.

