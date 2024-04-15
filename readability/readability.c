#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);


int main(void)
{
    string text = get_string("Text: ");
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);
    float L, S, index;
    L = ((float)letters / (float)words) * 100;
    S = ((float)sentences / (float)words) * 100;
    index = (0.0588 * L) - (0.296 * S) - 15.8;

    if ((int)round(index) >= 16)
    {
        printf("Grade 16+\n");
    }
    else if ((int)round(index) < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", (int)round(index));
    }
    return 0;
}

int count_letters(string text)
{
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (islower(text[i]) || isupper(text[i]))
        {
            count++;
        }
        else
        {
            continue;
        }
    }
    return count;
}

int count_words(string text)
{
    int count = 1;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] == ' ')
        {
            count++;
        }
        else
        {
            continue;
        }
    }
    return count;
}

int count_sentences(string text)
{
    int count = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            count++;
        }
    }
    return count;
}