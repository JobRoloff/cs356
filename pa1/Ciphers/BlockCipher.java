package Ciphers;

import java.io.File;
import java.io.FileInputStream;

public class BlockCipher {

    protected class Block {
        Block(byte[] data){
            this.data = data;
        }
        static int BLOCK_SIZE_BYTES = 16;
        private byte[] data;
    }

    public BlockCipher(File inputFile, File keyfile) {
        this.processFile(inputFile);
        this.keyFile=keyfile;
    }

    /**
     * split up file into blocks
     * 
     * @param inputFile
     */
    private void processFile(File inputFile) {
        try (FileInputStream fileInputStream = new FileInputStream(inputFile)) {
            byte[] buffer = new byte[Block.BLOCK_SIZE_BYTES];
            int bytesRead;

            while ((bytesRead = fileInputStream.read(buffer)) != -1) {
                if (bytesRead < Block.BLOCK_SIZE_BYTES) {
                    // padd last block
                    // Use 0x81 as the padding byte. Because the input file is in ASCII (in the case
                    // of plaintext) and the padding value (81 in hexadecimal or 129 in decimal)
                    // falls outside the ASCII (0-127) range, it allows us to distinguish padding
                    // bytes from plaintext bytes.
                    for (int i =bytesRead; i < Block.BLOCK_SIZE_BYTES; i++){
                        buffer[i] = (byte) 0x81;
                    } 
                }
                // process block (XOR then Swap)
            }
        } catch (Exception e) {
            // TODO: handle exception: FileNotFound, IOException
        }
    }

    /**
     * encrypt via XOR
     */
    public void encrypt() {
        // bitewise compare keyfile to block

    }

    /**
     * swap bytes for each XORed output (16 byte block)
     */
    private void swap(){
        byte startPointer;
        byte endPointer;

    }
    private Block[] blocks;
    private File keyFile;
}