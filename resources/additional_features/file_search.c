#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdbool.h>

int search_for_file_in_drive(char *dirname, char *searchTerm)
{
    DIR *dir; struct dirent *entry;

    if ((dir = opendir(dirname)) == NULL) { return 1; }

    while ((entry = readdir(dir)) != NULL) {
        char newdir[1024];
        sprintf(newdir, "%s\\%s", dirname, entry->d_name);
        bool isDir = entry->d_type == DT_DIR, 
            containsSearchTerm = strstr(entry->d_name, searchTerm) != NULL, 
            isDotDir = strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0;

        if (isDir) {
            if (isDotDir) continue;

            search_for_file_in_drive(newdir, searchTerm);
        }
        else if (containsSearchTerm) { printf("%s\n", newdir); }
    }

    closedir(dir);
    return 0;
}
int main(int argc, char *argv[]) {
    bool notEnoughArgs = argc < 3;
    if (notEnoughArgs) { return 1; }

    search_for_file_in_drive(argv[2], argv[1]);
    return 0;
}
