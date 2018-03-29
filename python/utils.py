def string_to_bytes(string):
    """
    Transforms a string of ascii text into a string of bytes representing the
    message
    """
    ret_bytes = 0
    for char in string:
        ret_bytes = ret_bytes << 8
        ret_bytes += ord(char)
    return ret_bytes

def bytes_to_string(byte_str):
    """
    Transforms a given string of bytes into corresponding ascii text
    """
    ret_str = ''
    while byte_str != 0:
        ch_code = byte_str & 255
        ret_str = chr(ch_code) + ret_str
        byte_str = byte_str >> 8
    return ret_str

# egcd and mulinv come from:
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
def gcd(a, b):
    """
    Uses the Euclidian Algorithm to find the greatest commmon divisor for a and
    b.

    Returns the largest integer c such that c divides a and c divides b.
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mult_inverse(b, n):
    """
    Finds the multiplicitive inverse of b, given mod n

    Returns an integer c such that cb (mod n) = 1
    """
    g, x, _ = gcd(b, n)
    if g == 1:
        return x % n
