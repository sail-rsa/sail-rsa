package sail;

import java.math.BigInteger;

public class Utils {

    public static BigInteger stringToBytes(String string) {
        BigInteger integer = BigInteger.ZERO;
        for (int i = 0; i < string.length(); i++) {
            char c = string.charAt(i);
            integer = integer.shiftLeft(8);
            integer = integer.add(new BigInteger((int)c + ""));
        }

        return integer;
    }

    public static String bytesToString(BigInteger val) {
        StringBuilder result = new StringBuilder();
        BigInteger twoFiftyFive = new BigInteger("255");

        while (!val.equals(BigInteger.ZERO)) {
            int charCode = val.and(twoFiftyFive).intValueExact();
            result.insert(0, (char)charCode);
            val = val.shiftRight(8);
        }

        return result.toString();
    }
}
