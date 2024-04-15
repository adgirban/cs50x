#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float avg = (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0;
            image[i][j].rgbtBlue = round(avg);
            image[i][j].rgbtGreen = round(avg);
            image[i][j].rgbtRed = round(avg);
        }
    }
    return;
}

// Convert image to sepia
int check (int a, int b)
{
    if (a >= b)
    {
        return 1;
    }
    return 0;
}

void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sepiaRed = .393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue;
            float sepiaGreen = .349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue;
            float sepiaBlue = .272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue;

            if(check ((int)sepiaRed, 255))
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = round(sepiaRed);
            }

            if(check ((int)sepiaGreen, 255))
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = round(sepiaGreen);
            }

            if(check ((int)sepiaBlue, 255))
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = round(sepiaBlue);
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width/2; j++)
        {
            temp[0][0] = image[i][j];
            image[i][j] = image[i][width-j-1];
            image[i][width-j-1] = temp[0][0];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    //copying all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float blue = 0;
            float red = 0;
            float green = 0;
            float boxes = 0;

            for (int r = i - 1; r < i + 2; r++)
            {
                for (int c = j - 1; c < j + 2; c++)
                {
                    if (r < 0 || c < 0 || r > height - 1 || c > width - 1)
                    {
                        continue;
                    }

                    blue += copy[r][c].rgbtBlue;
                    red += copy[r][c].rgbtRed;
                    green += copy[r][c].rgbtGreen;
                    boxes++;
                }
            }

            image[i][j].rgbtBlue = round(blue/boxes);
            image[i][j].rgbtGreen = round(green/boxes);
            image[i][j].rgbtRed = round(red/boxes);
        }
    }
    return;
}
