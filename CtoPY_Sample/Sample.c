#include <stdlib.h>
#include <stdio.h>
#include <string.h>

char* echo(char* s_in){
    char* des = malloc(sizeof(char) * (strlen(s_in) + strlen("root_return: ") +strlen("\n")+1));
    strcpy(des,"echo: ");
    strcat(des,s_in);
    strcat(des,"\n");
    return des;
}
