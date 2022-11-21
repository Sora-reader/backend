from ninja.security import APIKeyHeader


class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        if key == "supersecret":
            return key


api_key_auth = ApiKey()
