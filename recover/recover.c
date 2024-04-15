#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;
int const BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Incorrect Usage\n");
        return 1;
    }

    FILE *infile = fopen(argv[1], "r");
    if (infile == NULL)
    {
        printf("Could not open file\n");
        return 2;
    }

    BYTE block[BLOCK_SIZE];
    int count = 0;

    FILE *outfile = NULL;
    char outfile_name[8];

    while (fread(block, 1, BLOCK_SIZE, infile) == BLOCK_SIZE)
    {
        if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xf0) == 0xe0)
        {
            if (outfile != NULL)
            {
                fclose(outfile);
            }
            sprintf(outfile_name, "%03i.jpg", count);
            outfile = fopen(outfile_name, "w");
            count++;
        }
        if (outfile != NULL)
        {
            fwrite(block, 1, 512, outfile);
        }
    }

    fclose(outfile);
    fclose(infile);
    return 0;
}