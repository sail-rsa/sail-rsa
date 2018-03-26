from rsa_soln import encrypt, decrypt, generate_keys

p = 2 ** 2203 - 1
q = 2 ** 2281 - 1

e, d, n = generate_keys(p, q)
text = 'Hello, world!'

ciphertext_bytes = encrypt(text, e, n)
message = decrypt(ciphertext_bytes, d, n)

print(message)
