package Ciphers;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Arrays;

public class BlockCipher {

    public static final int BLOCK_SIZE_BYTES = 16;
    public static final byte PAD = (byte) 0x81;
    private final byte[] key;

    public BlockCipher(File keyFile) throws IOException {
        this.key = loadKey(keyFile);
    }

    public void encryptFile(File inputFile, File outputFile) throws IOException {
        try (
                InputStream in = new BufferedInputStream(new FileInputStream(inputFile));
                OutputStream out = new BufferedOutputStream(new FileOutputStream(outputFile));) {

            byte[] block = new byte[BLOCK_SIZE_BYTES];
            int bytesRead;
            while ((bytesRead = in.read(block)) != -1) {
                if (bytesRead < BLOCK_SIZE_BYTES) {
                    padBlock(block, bytesRead);
                }
                xorBlock(block);
                swapBlock(block);
                out.write(block, 0, BLOCK_SIZE_BYTES);
                Arrays.fill(block, (byte) 0);
            }
        } catch (Exception e) {
            // TODO: handle exception
        }

    }

    /**
     * reads ciphertext into block, mutate block in place, zero out the block, read
     * next ciphertext block using the one from earlier
     * 
     * @param inputFile
     * @param outputFile
     */
    public void decryptFile(File inputFile, File outputFile) {
        try (
                InputStream in = new BufferedInputStream(new FileInputStream(inputFile));
                OutputStream out = new BufferedOutputStream(new FileOutputStream(outputFile));) {
            byte[] block = new byte[BLOCK_SIZE_BYTES];

            // variable to remove padding from the final plaintext block
            byte[] previousPlainBlock = null;
            while (true) {
                int numBlocksRead = readBlock(in, block);
                if (numBlocksRead == -1)
                    break;
                if (numBlocksRead != BLOCK_SIZE_BYTES)
                    throw new IOException("Ciphertext length must be a multiple of 16 bytes");

                swapBlock(block);
                xorBlock(block);

                if (previousPlainBlock != null)
                    out.write(previousPlainBlock);

                // take a snapshot of the decrypted bytes before reusing / changing the block
                // such that we are getting the values rather than reference to the arrays
                previousPlainBlock = Arrays.copyOf(block, BLOCK_SIZE_BYTES);

                Arrays.fill(block, (byte) 0);
            }
            if (previousPlainBlock != null) {
                // enure we pad our last block
                int length = unpaddedLength(previousPlainBlock);
                out.write(previousPlainBlock, 0, length);
            }
        } catch (Exception e) {
            System.err.println("Decrypt File Exception: " + e);
            e.printStackTrace();
        }
    }

    private static byte[] loadKey(File keyFile) throws IOException {
        byte[] key = new byte[BLOCK_SIZE_BYTES];
        try (
                InputStream in = new BufferedInputStream(new FileInputStream(keyFile))) {
            // read key's blocks
            int keyBlockSize = readBlock(in, key);

            // handle too short key
            if (keyBlockSize != BLOCK_SIZE_BYTES)
                throw new IOException("Key must be 16 bytes.");
            // handle too long key
            if (in.read() != -1)
                throw new IOException("Key is too long, it must be exactly 16 bytes.");

        } catch (Exception e) {
            System.err.println("LoadKey Exception: " + e);
            e.printStackTrace();
        }
        return key;
    }

    /**
     * Ties to fill block up tto 16 byttes by repeatedly calling read until any of
     * the following:
     * A: we've reached 16 bytes
     * B: End of File before reading anything (returns -1)
     * B: End of File after reading at least one byte
     * 
     * @param in
     * @param block
     * @return number of bytes read by this functtion call
     */
    private static int readBlock(InputStream in, byte[] block) throws IOException {
        int offset = 0;
        while (offset < BLOCK_SIZE_BYTES) {
            int numBytesRead = in.read(block, offset, BLOCK_SIZE_BYTES - offset);
            // at end of file (-1), we return -1 if the offset is at its starting point.
            // otherwise we return wher the offset left off.
            if (numBytesRead == -1)
                return offset == 0 ? -1 : offset;
            offset += numBytesRead;
        }
        return offset;
    }

    /**
     * pads aka "fills" the rest of your block with our hard coded byte value
     * 
     * @param block
     * @param bytesRead
     */
    private static void padBlock(byte[] block, int bytesRead) {
        for (int i = bytesRead; i < BLOCK_SIZE_BYTES; i++) {
            block[i] = PAD;
        }
    }

    /**
     * loops through the block's bytes and pairwise raises each byte by our key's
     * byte
     */
    private void xorBlock(byte[] block) {
        for (int i = 0; i < BLOCK_SIZE_BYTES; i++) {
            block[i] = (byte) (block[i] ^ key[i]);
        }
    }

    /**
     * swap bytes for each XORed output (16 byte block)
     */
    private void swapBlock(byte[] block) {
        int startPointer = 0;
        int endPointer = BLOCK_SIZE_BYTES - 1;
        int keyIndex = 0;
        while (startPointer < endPointer) {
            int isEqualKey = (key[keyIndex] & 0xFF) % 2;
            // here if the keys are equal, we swap and continue the loop
            if (isEqualKey == 1) {
                byte tmp = block[startPointer];
                block[startPointer] = block[endPointer];
                block[endPointer] = tmp;
                endPointer--;
            }
            startPointer++;
            // continue moving the index of the key we're using to swap with the block
            keyIndex = (keyIndex + 1) % BLOCK_SIZE_BYTES;
        }

    }

    /**
     * returns the the count of 16 bytes - the number of bytes at the end of a given
     * block thats equal to our pad value
     */
    private static int unpaddedLength(byte[] lastPlain) {
        int i = BLOCK_SIZE_BYTES - 1;
        while (i >= 0 && lastPlain[i] == PAD)
            i--;
        return i + 1;
    }
}