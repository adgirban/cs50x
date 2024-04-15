# TODO
from cs50 import get_string

def main():
    text = get_string("Text: ")

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = (0.0588 * L) - (0.296 * S) - 15.8

    if round(index) >= 16:
        print("Grade 16+")
    elif round(index) < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {round(index)}")


def count_letters(text):
    count = 0
    for i in text:
        if i >= 'A' and i <= 'Z':
            count += 1
        elif i >= 'a' and i <= 'z':
            count += 1
        else:
            continue
    return count

def count_words(text):
    count = 1
    for i in text:
        if i == ' ':
            count += 1
        else:
            continue
    return count

def count_sentences(text):
    count = 0
    for i in text:
        if i == '.' or i == '!' or i == '?':
            count += 1
    return count

main()



