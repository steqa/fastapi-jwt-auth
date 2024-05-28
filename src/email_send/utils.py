from random import randint


def get_verification_code() -> int:
    return randint(100000, 999999)
