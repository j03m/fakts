# TIL - Rate limit can be retured via headers



Rate limiter headers
How does a client know whether it is being throttled? And how does a client know the number of allowed remaining requests before being throttled? The answer lies in HTTP response headers. The rate limiter returns the following HTTP headers to clients:

`X-Ratelimit-Remaining`: The remaining number of allowed requests within the window. 
`X-Ratelimit-Limit`: It indicates how many calls the client can make per time window.
`X-Ratelimit-Retry-After`: The number of seconds to wait until you can make a request again without being throttled.

When a user has sent too many requests, a 429 too many requests error and `X-Ratelimit-
Retry-After` header are returned to the client.