#include <stdio.h>

int main(int argc, char const *argv[]) {

    char a;

    printf("cao ni ma %p\n", &a);
    while(1) {
        scanf("%c", &a);
        printf("%c", a);
    }
    return 0;
}
// x 0xffffceaf