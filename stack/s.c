#include <stdio.h>



int main(int argc, char *argv[]) {

    char *a = argv[1];  

    int l = 0;
    int i = 0;
    char ch = a[i];
    while (ch) {
        l++;
        ch = a[++i];
    }
    

    printf("%d\n", l);


    printf("%s", a);
    
    return 0;
}
