#include <stdio.h>


int main(int argv, char *args[]) {
    char* caonima = args[1];
    int i = 0;
    int c = 0;
    scanf("%s", caonima);

    
    char ch = caonima[i];

    while (ch) {
        c++;

        ch = caonima[++i];
    }


    printf("%d\n", c);
    printf("%s", caonima);
    



    return 0;
}