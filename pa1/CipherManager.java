import java.io.File;
import Ciphers.BlockCipher;
/**
 * runs cipher: encryption / decription and type of cipher
 */
public class CipherManager {
    public void run(String cipherType, File inputFile, String outtputFilePath, File keyFile, String modeOfOperation){
        // TODO run the appropriate dependency
        if (cipherType.equals("B")){
            BlockCipher cipher = new BlockCipher(inputFile, keyFile);
            cipher.encrypt();
        } else {
            //
        }
    }
}
