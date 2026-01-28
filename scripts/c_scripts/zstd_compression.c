#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "zstd.h"
#include "zstd.c"

#include <openssl/evp.h>
#include <openssl/rand.h>
#include <openssl/err.h>

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

EXPORT int process_file(const char *src_file_path, const char *dst_file_path, const char *password);
EXPORT int deprocess_file(const char *src_file_path, const char *dst_file_path, const char *password);
EXPORT int AES_encrypt_file(const char *src_file, const char *dst_file, const char *password);
EXPORT int AES_decrypt_file(const char *src_file, const char *dst_file, const char *password);
EXPORT int ZSTD_compress_file(const char *src_file_path, const char *dst_file_path);
EXPORT int ZSTD_decompress_file(const char *src_file_path, const char *dst_file_path);


int process_file(const char *src_file_path, const char *dst_file_path, const char *password) {
    char temp_file[1024];
    snprintf(temp_file, sizeof(temp_file), "%s.tmp", dst_file_path);

    if (ZSTD_compress_file(src_file_path, temp_file) != 0)
        return 1;

    if (AES_encrypt_file(temp_file, dst_file_path, password) != 0) {
        remove(temp_file);
        return 2;
    }

    remove(temp_file);
    return 0;
}

int deprocess_file(
    const char *src_file_path,
    const char *dst_file_path,
    const char *password
) {
    //create a safe temporary file path
    char temp_file[1024];
    snprintf(temp_file, sizeof(temp_file), "%s.tmp", dst_file_path);

    //first, decrypt into the temp file
    if (AES_decrypt_file(src_file_path, temp_file, password) != 0) {
        return 1; // decryption failed
    }

    //then decompress from the temp file to the final destination
    if (ZSTD_decompress_file(temp_file, dst_file_path) != 0) {
        remove(temp_file); // clean up temp file on error
        return 2; // decompression failed
    }

    //clean up temp file
    remove(temp_file);

    return 0; //success
}

int ZSTD_compress_file(const char *src_file_path, const char *dst_file_path){

    FILE *src = fopen(src_file_path, "rb");
    if (src == NULL) {return 1;}

    FILE *dst = fopen(dst_file_path, "wb"); 
    if (dst == NULL) {fclose(src); return 1;}

    //initialising ZSTD compressor
    ZSTD_CStream* cstream = ZSTD_createCStream();
    int compressionLevel = 19;
    ZSTD_initCStream(cstream, compressionLevel);

    size_t inChunkSize = 1024*1024; // 1 mb input buffer
    size_t outBufferSize = ZSTD_CStreamOutSize(); 

    //2 different buffers for streaming (uncompressed and compressed)
    void* inBuffer = malloc(inChunkSize);
    void* outBuffer = malloc(outBufferSize);

    if (!inBuffer || !outBuffer) {return 1;}

    //compression loop
    size_t readSize;
    while ((readSize = fread(inBuffer, 1, inChunkSize, src)) > 0) {
        ZSTD_inBuffer input = { inBuffer, readSize, 0 };
        
        while (input.pos < input.size) {
            ZSTD_outBuffer output = { outBuffer, outBufferSize, 0 };
            size_t ret = ZSTD_compressStream(cstream, &output, &input);
            fwrite(outBuffer, 1, output.pos, dst);
        }
    }

    //flush remaining uncompressed data
    int finished = 0;
    while (!finished) {
        ZSTD_outBuffer output = { outBuffer, outBufferSize, 0 };
        size_t ret = ZSTD_endStream(cstream, &output);
        fwrite(outBuffer, 1, output.pos, dst);
        if (ret == 0) finished = 1;
    }


    //cleanup
    ZSTD_freeCStream(cstream);
    fclose(src);
    fclose(dst);
    free(inBuffer);
    free(outBuffer);

    return 0;
}

int ZSTD_decompress_file(const char *src_file_path, const char *dst_file_path)
{

    FILE *src = fopen(src_file_path, "rb");
    if (!src) { return 1; }

    FILE *dst = fopen(dst_file_path, "wb");
    if (!dst) { return 1; }

    
    //initialising ZSTD decompressor
    ZSTD_DStream* dstream = ZSTD_createDStream();
    if (!dstream) { fclose(src); fclose(dst); return 1; }
    ZSTD_initDStream(dstream);

    size_t inChunkSize = 1024*1024; //1 MB input
    size_t outBufferSize = ZSTD_DStreamOutSize(); //recommended output size

    //initialising buffers
    void* inBuffer = malloc(inChunkSize);
    void* outBuffer = malloc(outBufferSize);
    if (!inBuffer || !outBuffer) {return 1; }

    //decompression loop
    size_t readSize;
    while ((readSize = fread(inBuffer, 1, inChunkSize, src)) > 0) {
        ZSTD_inBuffer input = { inBuffer, readSize, 0 };

        while (input.pos < input.size) {
            ZSTD_outBuffer output = { outBuffer, outBufferSize, 0 };
            size_t ret = ZSTD_decompressStream(dstream, &output, &input);
            if (ZSTD_isError(ret)) {
                return 1;
            }
            fwrite(outBuffer, 1, output.pos, dst);
        }
    }

    //cleanup
    ZSTD_freeDStream(dstream);
    free(inBuffer);
    free(outBuffer);
    fclose(src);
    fclose(dst);

    return 0;
}

int AES_encrypt_file(
    const char *src_file,
    const char *dst_file,
    const char *password
) {
    FILE *in = fopen(src_file, "rb");
    FILE *out = fopen(dst_file, "wb");
    if (!in || !out) return 1;

    unsigned char salt[16];
    unsigned char iv[12];
    unsigned char key[32];

    //generate random salt and iv so each file is different even with same password
    if (RAND_bytes(salt, sizeof(salt)) != 1 ||
        RAND_bytes(iv, sizeof(iv)) != 1) {
        fclose(in); fclose(out);
        return 1;
    }

    //write salt and iv at the start of the file so we can use it for decryption
    fwrite(salt, 1, sizeof(salt), out);
    fwrite(iv, 1, sizeof(iv), out);

    //derive the key from the password using the salt
    if (!PKCS5_PBKDF2_HMAC(password, strlen(password),
                           salt, sizeof(salt),
                           100000, EVP_sha256(),
                           sizeof(key), key)) {
        fclose(in); fclose(out);
        return 1;
    }

    //create a new context for encryption
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) { fclose(in); fclose(out); return 1; }

    //initialize encryption with aes 256 gcm and set iv length
    if (1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL) ||
        1 != EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, sizeof(iv), NULL) ||
        1 != EVP_EncryptInit_ex(ctx, NULL, NULL, key, iv)) {
        EVP_CIPHER_CTX_free(ctx); fclose(in); fclose(out);
        return 1;
    }

    unsigned char inbuf[4096], outbuf[4096 + 16];
    int outlen;
    size_t read_bytes;

    //read the file in chunks and encrypt each chunk
    while ((read_bytes = fread(inbuf, 1, sizeof(inbuf), in)) > 0) {
        if (1 != EVP_EncryptUpdate(ctx, outbuf, &outlen, inbuf, read_bytes)) {
            EVP_CIPHER_CTX_free(ctx); fclose(in); fclose(out);
            return 1;
        }
        //write encrypted chunk to output file
        fwrite(outbuf, 1, outlen, out);
    }

    //finalize encryption and write any remaining bytes
    if (1 != EVP_EncryptFinal_ex(ctx, outbuf, &outlen)) {
        EVP_CIPHER_CTX_free(ctx); fclose(in); fclose(out);
        return 1;
    }
    fwrite(outbuf, 1, outlen, out);

    //get the authentication tag for gcm and write it at the end
    unsigned char tag[16];
    if (1 != EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, sizeof(tag), tag)) {
        EVP_CIPHER_CTX_free(ctx); fclose(in); fclose(out);
        return 1;
    }
    fwrite(tag, 1, sizeof(tag), out);

    //free the context and close files
    EVP_CIPHER_CTX_free(ctx);
    fclose(in);
    fclose(out);

    return 0;
}

int AES_decrypt_file(
    const char *src_file,
    const char *dst_file,
    const char *password
) {
    FILE *in = fopen(src_file, "rb");
    FILE *out = fopen(dst_file, "wb");
    if (!in || !out) return 1;

    unsigned char salt[16], iv[12], tag[16], key[32];

    //read the salt and iv from the file so we can derive the key
    if (fread(salt, 1, sizeof(salt), in) != sizeof(salt) ||
        fread(iv, 1, sizeof(iv), in) != sizeof(iv)) {
        fclose(in); fclose(out);
        return 1;
    }

    //derive the key from password and salt
    if (!PKCS5_PBKDF2_HMAC(password, strlen(password),
                           salt, sizeof(salt),
                           100000, EVP_sha256(),
                           sizeof(key), key)) {
        fclose(in); fclose(out);
        return 1;
    }

    //find out how much encrypted data there is
    fseek(in, 0, SEEK_END);
    long filesize = ftell(in);
    if (filesize < 16 + 12 + 16) { fclose(in); fclose(out); return 1; }
    long ciphertext_len = filesize - 16 - 12 - 16;
    fseek(in, 16 + 12, SEEK_SET); //skip salt and iv

    //create decryption context
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) { fclose(in); fclose(out); return 1; }

    //initialize decryption with aes 256 gcm and set iv length
    if (1 != EVP_DecryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL) ||
        1 != EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, sizeof(iv), NULL) ||
        1 != EVP_DecryptInit_ex(ctx, NULL, NULL, key, iv)) {
        EVP_CIPHER_CTX_free(ctx); fclose(in); fclose(out);
        return 1;
    }

    unsigned char inbuf[4096], outbuf[4096];
    int outlen;
    long remaining = ciphertext_len;

    //read chunks of encrypted data and decrypt each chunk
    while (remaining > 0) {
        size_t chunk = fread(inbuf, 1, (remaining > sizeof(inbuf)) ? sizeof(inbuf) : remaining, in);
        if (chunk <= 0) break;
        remaining -= chunk;
        if (1 != EVP_DecryptUpdate(ctx, outbuf, &outlen, inbuf, chunk)) {
            EVP_CIPHER_CTX_free(ctx); fclose(in); fclose(out); remove(dst_file);
            return 1;
        }
        //write decrypted chunk to output file
        fwrite(outbuf, 1, outlen, out);
    }

    //read the gcm tag at the end
    if (fread(tag, 1, sizeof(tag), in) != sizeof(tag)) {
        EVP_CIPHER_CTX_free(ctx); fclose(in); fclose(out); remove(dst_file);
        return 1;
    }
    if (1 != EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_TAG, sizeof(tag), tag)) {
        EVP_CIPHER_CTX_free(ctx); fclose(in); fclose(out); remove(dst_file);
        return 1;
    }

    //finalize decryption and check tag (authentication)
    int ret = EVP_DecryptFinal_ex(ctx, outbuf, &outlen);
    EVP_CIPHER_CTX_free(ctx);
    fclose(in);
    fclose(out);

    if (ret != 1) {
        //this means password is wrong or file was changed
        remove(dst_file);
        return 2;
    }

    return 0;
}