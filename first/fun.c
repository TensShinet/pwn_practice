#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>


void func(int key)
{
    char overflowme[32];
    puts("CAO WO:");
    fflush(stdout);
    gets(overflowme); // smash me!
    if (key == 0xcafebabe)
    {
        system("/bin/sh");
    }
    else
    {
        puts("Nah..");
        fflush(stdout);
    }
}


int main(int argc, char *argv[])
{
    gid_t gid = getegid();
    setresgid(gid, gid, gid);

    func(0x12345678);
    return 0;
}