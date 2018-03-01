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

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

# egcd and mulinv come from:
# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

p = 2 ** 2203 - 1
q = 2 ** 2281 - 1
n = p * q

# coprime to (p - 1)(q - 1), can be any number though
e = 65537
d = mulinv(e, (p - 1) * (q - 1))

text = '\"But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?\"'
m = string_to_bytes(text)
while m > n:
    text = text[:-1]
    m = string_to_bytes(text)
ciphertext = pow(m, e, n)
text = pow(ciphertext, d, n)

print(bytes_to_string(text))
