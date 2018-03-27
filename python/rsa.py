from utils import string_to_bytes, bytes_to_string, mult_inverse

def generate_keys(p, q):
    '''
    Given two large primes p and q, generates the requisite components of a
    RSA public and private key.

    n = pq
    ed (mod (p-1)(q-1)) = 1

    Returns a 3-tuple of (e, d, n)
    '''
    e, d, n = (0, 0, 0) # Placeholder
    # TODO Your code here
    return (e, d, n)

def encrypt(message, e, n):
    '''
    Given a string message, and a public key (e, n), encrypts the string message
    and produces the bytes representing the ciphertext.

    E(x) = x^e (mod n)

    Returns ciphertext, an integer
    '''
    ciphertext_bytes = 0 # Placeholder
    # TODO Your code here
    return ciphertext_bytes

def decrypt(ciphertext_bytes, d, n):
    '''
    Given bytes representing ciphertext, and a private key (d, n), decrypts the
    ciphertext and produces the original message.

    D(y) = y^d (mod n)

    Returns a string message
    '''
    message = '' # Placeholder
    # TODO Your code here
    return message
