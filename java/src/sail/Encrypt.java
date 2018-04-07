package sail;

import java.math.BigInteger;

public class Encrypt {

    public static void main(String[] args) {
        String message = args[0];
        BigInteger e = new BigInteger(args[1]);
        BigInteger n = new BigInteger(args[2]);

        BigInteger encypted = RSASoln.encrypt(message, e, n);
        System.out.println(encypted);
    }

}