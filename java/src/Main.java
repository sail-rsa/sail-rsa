import java.math.BigInteger;

public class Main {

    private static BigInteger stringToBytes(String string) {
        BigInteger integer = BigInteger.ZERO;
        for (int i = 0; i < string.length(); i++) {
            char c = string.charAt(i);
            integer = integer.shiftLeft(8);
            integer = integer.add(new BigInteger((int)c + ""));
        }

        return integer;
    }

    private static String bytesToString(BigInteger val) {
        StringBuilder result = new StringBuilder();
        BigInteger twoFiftyFive = new BigInteger("255");

        while (!val.equals(BigInteger.ZERO)) {
            int charCode = val.and(twoFiftyFive).intValueExact();
            result.insert(0, (char)charCode);
            val = val.shiftRight(8);
        }

        return result.toString();
    }

    public static void main(String[] args) {
        BigInteger p = (new BigInteger("2").pow(2203)).subtract(BigInteger.ONE);
        BigInteger q = (new BigInteger("2").pow(2281)).subtract(BigInteger.ONE);
        BigInteger n = p.multiply(q);

        BigInteger e = new BigInteger("65537");
        BigInteger d = e.modInverse((p.subtract(BigInteger.ONE)).multiply(q.subtract(BigInteger.ONE)));

        String text = "Lorem ipsum";
        BigInteger m = stringToBytes(text);
        BigInteger ciphertext = m.modPow(e, n);
        BigInteger decrypted = ciphertext.modPow(d, n);

        System.out.println(bytesToString(decrypted));
    }

}
