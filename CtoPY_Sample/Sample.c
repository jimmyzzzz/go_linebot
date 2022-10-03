#include <stdlib.h>
#include <stdio.h>
#include <string.h>

char* get_user_id(char* s_in){
    char* des = malloc(sizeof(char) * (strlen(s_in) + strlen("root_return: ") +strlen("\n")+1));
    strcpy(des,"get_user_id: ");
    strcat(des,s_in);
    strcat(des,"\n");
    return des;
}

char* get_root_cmd(char* s_in){
    char* des = malloc(sizeof(char) * (strlen(s_in) + strlen("root_return: ") +strlen("\n")+1));
    strcpy(des,"get_root_cmd: ");
    strcat(des,s_in);
    strcat(des,"\n");
    return des;
}

char* get_user_cmds(char* s_in){
    char* des = malloc(sizeof(char) * (strlen(s_in) + strlen("root_return: ") +strlen("\n")+1));
    strcpy(des,"get_user_cmds: ");
    strcat(des,s_in);
    strcat(des,"\n");
    return des;
}

char* echo(char* s_in){
    char* des = malloc(sizeof(char) * (strlen(s_in) + strlen("root_return: ") +strlen("\n")+1));
    strcpy(des,"echo: ");
    strcat(des,s_in);
    strcat(des,"\n");
    return des;
}

char* root_return(char* s_in){
    char* des = malloc(sizeof(char) * (strlen(s_in) + strlen("root_return: ") +strlen("\n")+1));
    strcpy(des,"root_return: ");
    strcat(des,s_in);
    strcat(des,"\n");
    return des;
}