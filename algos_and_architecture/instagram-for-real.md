### Data Modeling

#### 1. **Feed Item Table**
   - **Schema**:
     - `post_id`: Primary Key, unique identifier for each post.
     - `author_id`: Foreign Key, referencing the user who created the post.
     - `content`: Text content of the post.
     - `media_url`: URL reference to media (image or video).
     - `timestamp`: Timestamp of when the post was created.
     - `likes`: Count of likes for the post.
   - **Sample SQL**:
     ```sql
     CREATE TABLE feed_item (
         post_id SERIAL PRIMARY KEY,
         author_id INT REFERENCES users(user_id),
         content TEXT,
         media_url VARCHAR(255),
         timestamp TIMESTAMP,
         likes INT
     );
     ```

#### 2. **User Subscription Table**
   - **Schema**:
     - `user_id`: Foreign Key, referencing the user who is following.
     - `followed_user_id`: Foreign Key, referencing the user being followed.
   - **Sample SQL**:
     ```sql
     CREATE TABLE user_subscription (
         user_id INT REFERENCES users(user_id),
         followed_user_id INT REFERENCES users(user_id),
         PRIMARY KEY (user_id, followed_user_id)
     );
     ```

#### 3. **Sharding Strategy**
   - **Database Sharding**: Partition both the Feed Item Table and User Subscription Table across multiple database instances.
   - **Sharding Key**: Use `user_id` as the sharding key to ensure that all data related to a specific user resides in the same shard.
   - **Consistent Hashing**: Implement consistent hashing to distribute the data evenly across shards and minimize re-sharding when adding/removing database instances.

#### 4. **Caching Strategy**
   - **Distributed Cache**: Utilize a distributed cache like Redis to store pre-computed user feeds.
   - **Cache Key**: Use a combination of `user_id` and `cursor` as the cache key to uniquely identify different segments of the user's feed.
   - **Cache Invalidation**: Implement a strategy to invalidate or update the cache when new posts are added to the user's feed.

### Sample Code for Retrieving User Feed

Here's a Python code snippet that demonstrates how you might retrieve a user's feed from the database, considering sharding:

```python
def get_shard(user_id):
    # Determine the appropriate shard based on the user_id
    shard_key = hash(user_id) % NUM_SHARDS
    return database_shards[shard_key]

def retrieve_user_feed(user_id, cursor, batch_size):
    shard = get_shard(user_id)
    query = """
        SELECT * FROM feed_item
        WHERE author_id IN (SELECT followed_user_id FROM user_subscription WHERE user_id = %s)
        AND post_id < %s
        ORDER BY timestamp DESC
        LIMIT %s
    """
    return shard.execute(query, (user_id, cursor, batch_size))
```

This code first determines the appropriate shard based on the `user_id`, then executes a query to retrieve the user's feed, considering the user's subscriptions and applying cursor-based pagination.

### Cache Key Explanation

When implementing an infinite scroll feature, the user's feed is typically not loaded all at once. Instead, it's loaded in segments or "pages" as the user scrolls. This means that at any given time, you might need to retrieve a specific segment of the user's feed, starting from a particular point (the cursor) and containing a certain number of posts.

Caching these segments can significantly improve performance, especially if the same segments are requested frequently by the same or different users.

#### **Components of the Cache Key**
1. **`user_id`**: This identifies the specific user's feed. Different users will have different feeds based on their subscriptions, so the `user_id` ensures that the cache entry corresponds to the correct user.

2. **`cursor`**: This identifies the starting point of the segment within the user's feed. It could be a timestamp, post ID, or another value that indicates where this segment begins in the chronological order of posts. By including the cursor in the cache key, you can cache different segments of the user's feed separately.

### **Example of Cache Key Usage**
Imagine a user's feed that consists of 100 posts, and you're implementing infinite scroll with 20 posts per segment. You might cache these segments with keys like:

- `user123_cursor1`: Contains posts 1-20
- `user123_cursor21`: Contains posts 21-40
- `user123_cursor41`: Contains posts 41-60
- ... and so on.

When a request comes in for a specific segment of the user's feed, you can quickly check the cache using the appropriate key. If the segment is in the cache, you can return it immediately, avoiding a database query.

### **Code Snippet for Caching and Retrieval**
Here's a Python code snippet that demonstrates how you might use this cache key strategy with Redis:

```python
import redis

def get_cache_key(user_id, cursor):
    return f"user{user_id}_cursor{cursor}"

def retrieve_user_feed(user_id, cursor, batch_size):
    cache_key = get_cache_key(user_id, cursor)
    cached_feed = redis_client.get(cache_key)

    if cached_feed:
        return cached_feed

    # If not in cache, retrieve from database and store in cache
    feed_segment = query_feed_from_database(user_id, cursor, batch_size)
    redis_client.set(cache_key, feed_segment)

    return feed_segment
```

### **Conclusion**
By using a combination of `user_id` and `cursor` as the cache key, you can efficiently cache different segments of a user's feed, supporting the infinite scroll feature. This strategy can significantly reduce database load and improve response times, contributing to the overall scalability of the system.