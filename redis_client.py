import redis
import os

# Initialize Redis connection (this can be shared across other files)
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_password = os.getenv('REDIS_PASSWORD', None)

# Create the Redis client
redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
