#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int compare_files(FILE *fp1, FILE *fp2);

int main(void){
    char src_file_path[]="C:\\Users\\danie\\Documents\\Coding_projects\\LockBox\\media\\testing_files\\src.txt";
    char dst_file_path[]="C:\\Users\\danie\\Documents\\Coding_projects\\LockBox\\media\\testing_files\\restored.txt";
    FILE *src = fopen(src_file_path, "rb");
    FILE *dst = fopen(dst_file_path, "rb");

    if (src == NULL || dst == NULL){perror("couldnt open file"); return 1;}
    
    printf("Files are equal: %i\n", compare_files(src, dst));

    fclose(src);
    fclose(dst);
    return 0;
}

int compare_files(FILE *fp1, FILE *fp2){
    unsigned char buf1[4096], buf2[4096];
    size_t n1, n2;

    do {
        n1 = fread(buf1, 1, sizeof(buf1), fp1);
        n2 = fread(buf2, 1, sizeof(buf2), fp2);
        if (n1 != n2 || memcmp(buf1, buf2, n1) != 0) {return 0;} 
    } while(n1 > 0 && n2 > 0);

    if (n2 != n1) {return 0;}
    return 1;
}