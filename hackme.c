#include <stdio.h>
#include <string.h>

void print (char* s){
    char buffer[200];

    strcpy(buffer, s);
    printf("Anfang von Buffer: %p\n", buffer);
    printf("Ende von Buffer: %s\n", buffer);
}

int main(int argc, char** argv){
    printf("argc %d",argc);
    if(argc == 2) {
        print(argv[1]);
    }
    else {
        printf("Usage: %s <string>\n", argv[1]);
        printf("Bitte ein Argument übergeben. \n");
    }
    return 0; 
}