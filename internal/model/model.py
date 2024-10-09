from dataclasses import dataclass


@dataclass
class Client:
    hashed_key: str
    subscription_expiration_date: int
