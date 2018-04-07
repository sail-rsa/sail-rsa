package sail;

import java.math.BigInteger;

public class Decrypt {

    public static void main(String[] args) {
        BigInteger ciphertextBytes = new BigInteger(args[0]);
        BigInteger d = new BigInteger(args[1]);
        BigInteger n = new BigInteger(args[2]);

        String message = RSASoln.decrypt(ciphertextBytes, d, n);
        System.out.println(message);
    }

}