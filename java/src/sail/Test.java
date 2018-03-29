package sail;

import java.math.BigInteger;

public class Test {

    public static void main(String[] args) {
        BigInteger p = (new BigInteger("2").pow(2203)).subtract(BigInteger.ONE);
        BigInteger q = (new BigInteger("2").pow(2281)).subtract(BigInteger.ONE);

        Tuple3 keys = RSA.generateKeys(p, q);
        BigInteger e = keys.first;
        BigInteger d = keys.second;
        BigInteger n = keys.third;

        String text = "Hello, world!";
        BigInteger ciphertextBytes = RSA.encrypt(text, e, n);
        String message = RSA.decrypt(ciphertextBytes, d, n);

        System.out.println(message);
    }

}
