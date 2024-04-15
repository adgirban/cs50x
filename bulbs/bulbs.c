#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    // TODO
    string text = get_string("Message: ");
    int arr[BITS_IN_BYTE];
    for (int i = 0; text[i] != '\0'; i++)
    {
        int dec = text[i];
        int count = 0;
        while (dec != 0)
        {
            if (dec % 2 == 0)
            {
                arr[count] = 0;
                dec /= 2;
                count++;
            }
            else
            {
                arr[count] = 1;
                dec /= 2;
                count++;
            }
        }
        while (count != BITS_IN_BYTE)
        {
            arr[count] = 0;
            count++;
        }

        for (int j = BITS_IN_BYTE - 1; j >= 0; j--)
        {
            print_bulb(arr[j]);
        }
        printf("\n");
    }
    return 0;
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
