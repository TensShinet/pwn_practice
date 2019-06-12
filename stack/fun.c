#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

void vun(char a[]) {
    char b[10];
    strcpy(b, a);
}
int main() {
    char a[100];
    puts("cao wo: ");
    fflush(stdout);
    gets(a);
    vun(a);
    
    return 0;
}