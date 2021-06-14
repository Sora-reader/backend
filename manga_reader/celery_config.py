from os import environ

REDIS_URL = environ.get("REDIS_URL")

broker_url = REDIS_URL
result_backend = broker_url
timezone = "UTC"
