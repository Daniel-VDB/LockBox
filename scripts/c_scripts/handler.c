#include <stdio.h>

//compiling a c file to be used in python: gcc -shared -o handler.dll handler.c

__declspec(dllexport) void say_hello(char *x) {
    printf("Hello, %s!\n", x);
}