#include <stdio.h>
#include <dirent.h>
#include <string.h>

int search_for_file_in_drive(char *dirname, char *searchTerm)
{
    DIR *dir;
    struct dirent *entry;
    if ((dir = opendir(dirname)) == NULL)
    {
        return 1;
    }
    while ((entry = readdir(dir)) != NULL)
    {
        char newdir[1024];
        sprintf(newdir, "%s\\%s", dirname, entry->d_name);

        if (entry->d_type == DT_DIR)
        {
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
                continue;
            search_for_file_in_drive(newdir, searchTerm);
        }
        else
        {
            // if entry name contains searchTerm, print it
            if (strstr(entry->d_name, searchTerm) != NULL)
            {
                printf("%s\n", newdir);
            }
        }
    }
    closedir(dir);
    return 0;
}
int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        return 1;
    }
    search_for_file_in_drive(argv[2], argv[1]);
    return 0;
}