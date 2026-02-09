import java.io.File;

/**
 * runs cipher: encryption / decription and type of cipher
 */
public class CipherManager {
    public void run(String cipherType, File inputFile, String outputFilePath, File keyFile, String modeOfOperation) {

        ICipher cipher = null;

        if (cipherType.equals("B")) {
            try {
                cipher = new BlockCipher(keyFile);
            } catch (Exception e) {
                System.err.println("Cipher Manager Block Error: ");
                e.printStackTrace();
            }
        } else if (cipherType.equals("S")) {
            try {
                cipher = new StreamCipher(keyFile);
            } catch (Exception e) {
                System.err.println("Cipher Manager Block Error: ");
                e.printStackTrace();
            }
        
        }
        cipher.run(inputFile, outputFilePath, modeOfOperation);
    }
}
