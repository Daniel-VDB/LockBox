#include <stdio.h>
#include <stdlib.h>

#define ZSTD_STATIC_LINKING_ONLY
#include "zstd.h"
#include "zstd.c"


int ZSTD_compress_file(void);
int ZSTD_decompress_file(void);

int main(void)
{
    ZSTD_compress_file();
    ZSTD_decompress_file();
}

int ZSTD_compress_file(void){
    // opening file and creating desination
    char src_file_path[]="C:\\Users\\danie\\Documents\\Coding_projects\\LockBox\\media\\testing_files\\src.txt";
    char dst_file_path[]="C:\\Users\\danie\\Documents\\Coding_projects\\LockBox\\media\\testing_files\\dst.zst"; //compressed file

    FILE *src = fopen(src_file_path, "rb");
    if (src == NULL) {perror("Error; couldn't open source"); return 1;}

    FILE *dst = fopen(dst_file_path, "wb"); 
    if (dst == NULL) {fclose(src); perror("Error; couldn't open destination"); return 1;}

    // initialising ZSTD compressor
    ZSTD_CStream* cstream = ZSTD_createCStream();
    int compressionLevel = 19;
    ZSTD_initCStream(cstream, compressionLevel);

    size_t inChunkSize = 1024*1024; // 1 mb input buffer
    size_t outBufferSize = ZSTD_CStreamOutSize(); 

    // 2 different buffers for streaming (uncompressed and compressed)
    void* inBuffer = malloc(inChunkSize);
    void* outBuffer = malloc(outBufferSize);

    if (!inBuffer || !outBuffer) { perror("malloc"); return 1;}

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

    
    printf("Compression complete: %s --> %s\n", src_file_path, dst_file_path);
    return 0;
}

int ZSTD_decompress_file(void)
{
    char src_file_path[] = "C:\\Users\\danie\\Documents\\Coding_projects\\LockBox\\media\\testing_files\\dst.zst";
    char dst_file_path[] = "C:\\Users\\danie\\Documents\\Coding_projects\\LockBox\\media\\testing_files\\restored.txt";

    FILE *src = fopen(src_file_path, "rb");
    if (!src) { perror("Error opening compressed source"); return 1; }

    FILE *dst = fopen(dst_file_path, "wb");
    if (!dst) { fclose(src); perror("Error opening destination"); return 1; }

    
    // initialising ZSTD decompressor
    ZSTD_DStream* dstream = ZSTD_createDStream();
    if (!dstream) { fclose(src); fclose(dst); perror("Failed to create ZSTD_DStream"); return 1; }
    ZSTD_initDStream(dstream);

    size_t inChunkSize = 1024*1024; // 1 MB input
    size_t outBufferSize = ZSTD_DStreamOutSize(); // recommended output size

    // initialising buffers
    void* inBuffer = malloc(inChunkSize);
    void* outBuffer = malloc(outBufferSize);
    if (!inBuffer || !outBuffer) { perror("malloc"); return 1; }

    // decompression loop
    size_t readSize;
    while ((readSize = fread(inBuffer, 1, inChunkSize, src)) > 0) {
        ZSTD_inBuffer input = { inBuffer, readSize, 0 };

        while (input.pos < input.size) {
            ZSTD_outBuffer output = { outBuffer, outBufferSize, 0 };
            size_t ret = ZSTD_decompressStream(dstream, &output, &input);
            if (ZSTD_isError(ret)) {
                fprintf(stderr, "Decompression error: %s\n", ZSTD_getErrorName(ret));
                return 1;
            }
            fwrite(outBuffer, 1, output.pos, dst);
        }
    }

    // cleanup
    ZSTD_freeDStream(dstream);
    free(inBuffer);
    free(outBuffer);
    fclose(src);
    fclose(dst);

    printf("Decompression complete: %s --> %s\n", src_file_path, dst_file_path);
    return 0;
}