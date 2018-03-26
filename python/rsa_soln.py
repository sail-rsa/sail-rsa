from utils import string_to_bytes, bytes_to_string, mult_inverse

def generate_keys(p, q):
    n = p * q
    e = 65537
    d = mult_inverse(e, (p - 1) * (q - 1))
    return (e, d, n)

def encrypt(message, e, n):
    message_bytes = string_to_bytes(message)
    ciphertext_bytes = pow(message_bytes, e, n)
    return ciphertext_bytes

def decrypt(ciphertext_bytes, d, n):
    message_bytes = pow(ciphertext_bytes, d, n)
    message = bytes_to_string(message_bytes)
    return message
