
import java.io.File;

class Cipher {
    public static void main(String args[]) {
        if (args.length != 5){
            System.err.println("Usage: java Cipher <B|C> <inputFile> <outputFile> <keyFile> <E|D>");
            System.exit(1);
        }

        String cipherType = args[0];
        if (!cipherType.equals("B") && !cipherType.equals("C")) {
            System.err.print("Invalid Function Type");
            System.exit(1);
        }

        File inputFile = new File(args[1]);
        if (!inputFile.exists()) {
            System.err.print("Input File Does Not Exist");
            System.exit(1);
        }

        String outputFilePath = args[2];
        
        File keyFile = new File(args[3]);
        if (!keyFile.exists()) {
            System.err.print("Key File Does Not Exist");
            System.exit(1);
        }
        // if block, contents can only be 16 bytets
        // if stream, contents can be ANY length

        String modeOfOperation = args[4];
        if (!modeOfOperation.equals("E") && !modeOfOperation.equals("D")){
            System.err.print("Invalid Mode Type");
            System.exit(1);
        }

        CipherManager cipherManager = new CipherManager();
        cipherManager.run(cipherType, inputFile, outputFilePath, keyFile, modeOfOperation);
    }

}
