def string_to_bytes(s):
    val = 0
    for ch in s:
        val = val << 8
        val += ord(ch)
    return val

def bytes_to_string(val):
    s = ''
    while val != 0:
        ch_code = val & 255
        s = chr(ch_code) + s
        val = val >> 8
    return s

# egcd and mulinv come from:
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
def gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mult_inverse(b, n):
    g, x, _ = gcd(b, n)
    if g == 1:
        return x % n
