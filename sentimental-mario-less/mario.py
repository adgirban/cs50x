# TODO

while True:
    try:
        height = int(input('Height: '))
        if height > 0 and height < 9:
            break
    except ValueError:
        print(end = '')

for i in range(height):
    for j in range(height):
        if j >= height-i-1:
            print('#', end='')
        else:
            print(' ', end='')
    print()
