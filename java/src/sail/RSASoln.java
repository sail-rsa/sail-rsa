package sail;

import java.math.BigInteger;

public class RSASoln {

    /**
     * Given two large primes p and q, generates the requisite components of a
     * RSA public and private key.
     *
     * n = pq
     * ed (mod (p-1)(q-1)) = 1
     *
     * @param p First large prime
     * @param q Second large prime
     * @return  3-tuple of (e, d, n)
     */
    public static Tuple3 generateKeys(BigInteger p, BigInteger q) {

        BigInteger n = p.multiply(q);
        BigInteger p1q1 = (p.subtract(BigInteger.ONE)).multiply(q.subtract(BigInteger.ONE));
        BigInteger e = new BigInteger("65537");
        BigInteger d = e.modInverse(p1q1);

        return new Tuple3(e, d, n);
    }

    /**
     * Given a string message, and a public key (e, n), encrypts the string message
     * and produces the bytes representing the ciphertext.
     *
     * E(x) = x^e (mod n)
     *
     * @param message Message, as a string
     * @param e       Exponent portion of public key
     * @param n       Modulus component of public key
     * @return        Ciphertext, a BigInteger
     */
    public static BigInteger encrypt(String message, BigInteger e, BigInteger n) {

        BigInteger messageBytes = Utils.stringToBytes(message);
        BigInteger ciphertextBytes = messageBytes.modPow(e, n);

        return ciphertextBytes;
    }

    /**
     * Given bytes representing ciphertext, and a private key (d, n), decrypts the
     * ciphertext and produces the original message.
     *
     * D(y) = y^d (mod n)
     *
     * @param ciphertextBytes Ciphertext, as a BigInteger
     * @param d               Exponent portion of private key
     * @param n               Modulus component of private key
     * @return                Message, a String
     */
    public static String decrypt(BigInteger ciphertextBytes, BigInteger d, BigInteger n) {

        BigInteger messageBytes = ciphertextBytes.modPow(d, n);
        String message = Utils.bytesToString(messageBytes);

        return message;
    }

}
