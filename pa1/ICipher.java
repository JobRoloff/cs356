import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;

public interface ICipher {
    File getKeyFile();
    void run(File inputFile, String outputFilePath, String modeOfOperation);

    default void ensureParentDirExists(File outputFile) throws IOException{
        File parent = outputFile.getParentFile();
        if (parent != null && !parent.exists()){
            throw new IOException("Output directory does not exist: " + parent.getAbsolutePath());
        }
    }

    default void ensureFileExists(File outputFile) throws IOException{
        ensureParentDirExists(outputFile);
        if(!outputFile.exists()){
            if (!outputFile.createNewFile()){
                throw new IOException("Failed to createt output file: " + outputFile.getAbsolutePath());
            }
        }
    }
    
    default byte[] readAllKeyBytes() throws IOException {
        File keyFile = getKeyFile();
        if (keyFile == null) throw new IOException("Key file is null.");
        if (!keyFile.exists() || !keyFile.isFile()) throw new IOException("Key file not found or not a file." + keyFile.getAbsolutePath());
        
        byte[] bytes = Files.readAllBytes(keyFile.toPath());
        if (bytes.length == 0) throw new IOException("Key file is empty" + keyFile.getAbsolutePath());
        return bytes;
    }
    
    default byte[] readAllKeyBytesExact(int n) throws IOException {
        File keyFile = getKeyFile();
        if (keyFile == null) throw new IOException("Key file is null.");
        if (!keyFile.exists() || !keyFile.isFile()) throw new IOException("Key file not found or not a file." + keyFile.getAbsolutePath());
        
        byte[] key = new byte[n];
        try (InputStream in = new BufferedInputStream(new FileInputStream(keyFile))){
            int offset = 0;
            while (offset < n) {
                int r = in.read(key, offset, n-offset);
                if (r == -1) break;
                offset += r;
            }
            if (offset != n){
                throw new IOException("Key must be exactlly " + n + " bytes (got " + offset + " ).");
            }
            if (in.read() != -1){
                throw new IOException("Key is too long; must be exactly " + n + " bytes");
            }
        }
        if (key.length == 0) throw new IOException("Key file is empty" + keyFile.getAbsolutePath());
        return key;
    }

    default boolean isEncrypt(String mode){ return "E".equals(mode); }
    default boolean isDecrypt(String mode){ return "D".equals(mode); }
}
