import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;


public class StreamCipher implements ICipher {
    private final File keyFile;

    public StreamCipher(File keyfile) {
        this.keyFile = keyfile;
    }
    @Override
    public File getKeyFile(){
        return keyFile;
    }

    @Override
    public void run(File inputFile, String outputFilePath, String modeOfOperation) {
        // ensure output exists for both e and d modes
        File outputFile = new File(outputFilePath);
        File parent = outputFile.getParentFile();
        try {
            if (parent != null && !parent.exists()) {
                throw new IOException("Failed to create output directory: " + parent.getAbsolutePath());
            }
            if (!outputFile.exists()) {
                if (!outputFile.createNewFile()) {
                    throw new IOException("Failed to create output file: " + outputFile.getAbsolutePath());
                }
            }

        } catch (Exception e) {
            System.err.println("Error: something went wrong ensuring outputt file exists for both modes: e and d");
        }

        // Regardless of mode of operation, the stream cipher uses the same stuff under
        // the hood. Here we'll keep tthe control flow just for more descriptivee error
        // error printing

        if (modeOfOperation.equals("E")) {
            try {
                this.handleCipherFileStream(inputFile, outputFile);
            } catch (Exception e) {
                System.err.println("Error: Stream Cipher Run Encryption" + "\n" + "Message: " + e.getMessage());
            }
        } else if (modeOfOperation.equals("D")) {
            try {
                this.handleCipherFileStream(inputFile, outputFile);
            } catch (Exception e) {
                System.err.println("Error: Stream Cipher Run Decryption" + "\n" + "Message: " + e.getMessage());
            }

        }

    }

    public void handleCipherFileStream(File inputFile, File outputFile) throws IOException{
        // get key from file
        byte[] keyBytes = readAllKeyBytes();
        if (keyBytes.length == 0){ throw new IOException("Key is empty");}
        // create stream from inputFile
        try (
            InputStream in = new BufferedInputStream(new FileInputStream(inputFile));
            OutputStream out = new BufferedOutputStream(new FileOutputStream(outputFile, false))
        ){
            // pairwise xor bytes / chars from input file with thatt of the keyfile starting
            // from leftmost byte / index 0 for both
            // *note traversing the keyfile must be done such that the end of the key cycles
            // back to the start of the keyfile
            int keyIndex = 0;
            int b;
            while ((b = in.read()) != -1){
                int kb = keyBytes[keyIndex] & 0xFF;
                out.write((b^kb) & 0xFF);
                keyIndex++;
                if(keyIndex == keyBytes.length) keyIndex = 0;
            }
            out.flush();
        }

    }

}