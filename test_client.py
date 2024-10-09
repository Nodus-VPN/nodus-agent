import hashlib
import hmac


def hashing(user_key: str, hash_key: str) -> str:
    return hmac.new(hash_key.encode(), user_key.encode(), hashlib.sha256).hexdigest()


user_key = 'admin'
hash_key = "city"

hashed_user_key = hashing(user_key, hash_key)
print(hashed_user_key)
