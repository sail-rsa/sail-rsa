package sail;

import java.math.BigInteger;

public class GenKeys {

    public static void main(String[] args) {
        BigInteger prime1 = new BigInteger(args[0]);
        BigInteger prime2 = new BigInteger(args[1]);

        Tuple3 tuple = RSASoln.generateKeys(prime1, prime2);
        System.out.println(tuple);
    }

}
