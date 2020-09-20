import argparse
import random
import time


def read_start():
    importer = argparse.ArgumentParser(description='Крестики - нолики')
    importer.add_argument('size', type=int, help='Введите размер поля')
    importer.add_argument('win', type=int, help='Введите размер поля')
    importer.add_argument('gamemode', type=int, help='Введите размер поля')
    args = importer.parse_args()
    return args.size, args.win, args.gamemode


def visual(arr):
    print("┌───", end="")
    for i in range(len(arr) - 1):
        print("┬───", end="")
    print("┐")

    for i in arr[:-1]:
        for j in i:
            print("│", j, sep=" ", end=" ")
        print("│")
        print("├───", end="")
        for j in range(len(i) - 1):
            print("┼───", end="")
        print("┤")
    for j in arr[-1]:
        print("│", j, sep=" ", end=" ")
    print("│")
    print("└───", end="")
    for j in range(len(arr) - 1):
        print("┴───", end="")
    print("┘")


def gg_wp(arr, win, last):
    x = last[0]
    y = last[1]
    size = len(arr)
    key = arr[x][y]
    seek_y_bot = size - x - 1
    seek_y_top = x
    seek_x_left = y
    seek_x_right = size - y - 1

    counter = 1
    for i in range(seek_y_top):
        # print("T", arr[x - i - 1][y], counter)
        if arr[x - i - 1][y] == key:
            counter += 1
        else:
            break

    for i in range(seek_y_bot):
        # print("B", arr[x + i + 1][y], counter)
        if arr[x + i + 1][y] == key:
            counter += 1
        else:
            break
    if counter >= win:
        return key

    counter = 1
    for i in range(seek_x_left):
        # print("L", arr[x][y - i - 1], counter)
        if arr[x][y - i - 1] == key:
            counter += 1
        else:
            break

    for i in range(seek_x_right):
        # print("R", arr[x][y + i + 1], counter)
        if arr[x][y + i + 1] == key:
            counter += 1
        else:
            break
    if counter >= win:
        return key

    counter = 1
    for i in range(min(seek_x_left, seek_y_top)):
        # print("LT", arr[x - i - 1][y - i - 1], counter)
        if arr[x - i - 1][y - i - 1] == key:
            counter += 1
        else:
            break

    for i in range(min(seek_x_right, seek_y_bot)):
        # print("RB", arr[x + i + 1][y + i + 1], counter)
        if arr[x + i + 1][y + i + 1] == key:
            counter += 1
        else:
            break
    if counter >= win:
        return key

    counter = 1
    for i in range(min(seek_x_left, seek_y_bot)):
        # print("LB", arr[x + i + 1][y - i - 1], counter)
        if arr[x + i + 1][y - i - 1] == key:
            counter += 1
        else:
            break

    for i in range(min(seek_x_right, seek_y_top)):
        # print("RT", arr[x - i - 1][y + i + 1], counter)
        if arr[x - i - 1][y + i + 1] == key:
            counter += 1
        else:
            break
    if counter >= win:
        return key

    return 0


def human_turn(hod, arr, win):
    x, y = map(int, input().split())
    x -= 1
    y -= 1
    # print(x, y)
    if hod % 2 == 0:
        arr[x][y] = "x"
    else:
        arr[x][y] = "o"
    visual(arr)
    end = gg_wp(arr, win, [x, y])
    # print(end)
    if end != 0:
        print("Opa f5, " + end + " WINS!")
        return 0
    return arr, [x, y]


def animal_turn(hod, arr, win, last=[]):
    debug = 0
    size = len(arr)
    if hod % 2 == 0:
        key = "x"
    else:
        key = "o"
    if hod == 0:
        x = random.randint(1, len(arr) - 2)
        y = random.randint(1, len(arr) - 2)
        arr[x][y] = "x"
        visual(arr)
        return arr, [x, y]
    x = last[0]
    y = last[1]
    seek_y_bot = size - x - 1
    seek_y_top = x
    seek_x_left = y
    seek_x_right = size - y - 1

    weigth_arr = [[win ** 2 for j in range(len(arr))] for i in range(len(arr))]
    for i in range(len(weigth_arr)):
        for j in range(len(weigth_arr[i])):
            if arr[i][j] != ".":
                weigth_arr[i][j] += (10000 + win) ** 2
    if debug:
        print(key * 15)
        if input() == "exit":
            exit(0)
        visual(weigth_arr)
    check_arr = [[True for j in range(len(arr))] for i in range(len(arr))]
    for i in range(size):
        for j in range(size):
            if arr[i][j] == ".":
                check_arr[i][j] = False
    for i in range(size):
        for j in range(size):
            x, y = i, j
            seek_y_bot = size - x - 1
            seek_y_top = x
            seek_x_left = y
            seek_x_right = size - y - 1
            if check_arr[x][y]:
                if debug:
                    print("TB", x, y, key)
                    visual(weigth_arr)
                check_arr[x][y] = False
                key = arr[x][y]
                counter = 1
                for i in range(seek_y_top):
                    # print("T", arr[x - i - 1][y], counter)
                    if arr[x - i - 1][y] == key:
                        check_arr[x - i - 1][y] = False
                        counter += 1
                    else:
                        break
                for i in range(seek_y_bot):
                    # print("B", arr[x + i + 1][y], counter)
                    if arr[x + i + 1][y] == key:
                        check_arr[x + i + 1][y] = False
                        counter += 1
                    else:
                        break
                for i in range(seek_y_top):
                    # print("T", arr[x - i - 1][y], counter)
                    if arr[x - i - 1][y] == key:
                        continue
                    else:
                        weigth_arr[x - i - 1][y] -= counter ** 3
                        break
                for i in range(seek_y_bot):
                    # print("B", arr[x + i + 1][y], counter)
                    if arr[x + i + 1][y] == key:
                        continue
                    else:
                        weigth_arr[x + i + 1][y] -= counter ** 3
                        break

    check_arr = [[True for j in range(len(arr))] for i in range(len(arr))]
    for i in range(size):
        for j in range(size):
            if arr[i][j] == ".":
                check_arr[i][j] = False
    # 13212312312213
    for i in range(size):
        for j in range(size):
            x, y = i, j
            seek_y_bot = size - x - 1
            seek_y_top = x
            seek_x_left = y
            seek_x_right = size - y - 1
            if check_arr[x][y]:
                if debug:
                    print("LR", x, y, key)
                    visual(weigth_arr)
                check_arr[x][y] = False
                key = arr[x][y]
                counter = 1
                for i in range(seek_x_left):
                    # print("L", arr[x][y - i - 1], counter)
                    if arr[x][y - i - 1] == key:
                        check_arr[x][y - i - 1] = False
                        counter += 1
                    else:
                        break
                for i in range(seek_x_right):
                    # print("R", arr[x][y + i + 1], counter)
                    if arr[x][y + i + 1] == key:
                        check_arr[x][y - i - 1] = False
                        counter += 1
                    else:
                        break
                for i in range(seek_x_left):
                    # print("L", arr[x][y - i - 1], counter)
                    if arr[x][y - i - 1] == key:
                        continue
                    else:
                        weigth_arr[x][y - i - 1] -= counter ** 3
                        break
                for i in range(seek_x_right):
                    # print("R", arr[x][y + i + 1], counter)
                    if arr[x][y + i + 1] == key:
                        continue
                    else:
                        weigth_arr[x][y + i + 1] -= counter ** 3
                        break
    check_arr = [[True for j in range(len(arr))] for i in range(len(arr))]
    for i in range(size):
        for j in range(size):
            if arr[i][j] == ".":
                check_arr[i][j] = False
    # 12312321321123123
    for i in range(size):
        for j in range(size):
            x, y = i, j
            seek_y_bot = size - x - 1
            seek_y_top = x
            seek_x_left = y
            seek_x_right = size - y - 1
            if check_arr[x][y]:
                if debug:
                    print("LTRB", x, y, key)
                    visual(weigth_arr)
                check_arr[x][y] = False
                key = arr[x][y]
                counter = 1
                for i in range(min(seek_x_left, seek_y_top)):
                    # print("LT", arr[x - i - 1][y - i - 1], counter)
                    if arr[x - i - 1][y - i - 1] == key:
                        check_arr[x - i - 1][y - i - 1] = False
                        counter += 1
                    else:
                        break
                for i in range(min(seek_x_right, seek_y_bot)):
                    # print("RB", arr[x + i + 1][y + i + 1], counter)
                    if arr[x + i + 1][y + i + 1] == key:
                        check_arr[x + i + 1][y + i + 1] = False
                        counter += 1
                    else:
                        break
                for i in range(min(seek_x_left, seek_y_top)):
                    # print("LT", arr[x - i - 1][y - i - 1], counter)
                    if arr[x - i - 1][y - i - 1] == key:
                        continue
                    else:
                        weigth_arr[x - i - 1][y - i - 1] -= counter ** 3
                        break
                for i in range(min(seek_x_right, seek_y_bot)):
                    # print("RB", arr[x + i + 1][y + i + 1], counter)
                    if arr[x + i + 1][y + i + 1] == key:
                        continue
                    else:
                        weigth_arr[x + i + 1][y + i + 1] -= counter ** 3
                        break
    check_arr = [[True for j in range(len(arr))] for i in range(len(arr))]
    for i in range(size):
        for j in range(size):
            if arr[i][j] == ".":
                check_arr[i][j] = False
    # 154545415145
    for i in range(size):
        for j in range(size):
            x, y = i, j
            seek_y_bot = size - x - 1
            seek_y_top = x
            seek_x_left = y
            seek_x_right = size - y - 1
            if check_arr[x][y]:
                if debug:
                    print("LBRT", x, y, key)
                    visual(weigth_arr)
                check_arr[x][y] = False
                key = arr[x][y]
                counter = 1
                for i in range(min(seek_x_left, seek_y_bot)):
                    # print("LB", arr[x + i + 1][y - i - 1], counter)
                    if arr[x + i + 1][y - i - 1] == key:
                        check_arr[x + i + 1][y - i - 1] = False
                        counter += 1
                    else:
                        break
                for i in range(min(seek_x_right, seek_y_top)):
                    # print("RT", arr[x - i - 1][y + i + 1], counter)
                    if arr[x - i - 1][y + i + 1] == key:
                        check_arr[x - i - 1][y + i + 1] = False
                        counter += 1
                    else:
                        break
                for i in range(min(seek_x_left, seek_y_bot)):
                    # print("LB", arr[x + i + 1][y - i - 1], counter)
                    if arr[x + i + 1][y - i - 1] == key:
                        continue
                    else:
                        weigth_arr[x + i + 1][y - i - 1] -= counter ** 3
                        break
                for i in range(min(seek_x_right, seek_y_top)):
                    # print("RT", arr[x - i - 1][y + i + 1], counter)
                    if arr[x - i - 1][y + i + 1] == key:
                        continue
                    else:
                        weigth_arr[x - i - 1][y + i + 1] -= counter ** 3
                        break

    if hod % 2 == 0:
        key = "x"
    else:
        key = "o"
    #visual(weigth_arr)
    minimal = min(map(min, weigth_arr))
    flag = False
    for i in range(len(weigth_arr)):
        for j in range(len(weigth_arr[i])):
            if weigth_arr[i][j] == minimal:
                arr[i][j] = key
                x, y = i, j
                flag = True
                break
        if flag:
            break
    visual(arr)
    end = gg_wp(arr, win, [x, y])
    # print(end)
    if end != 0:
        print("Opa f5, " + end + " WINS!")
        return 0
    return arr, last


def game(inp):
    size, win, gamemode = inp
    arr = [["." for j in range(size)] for i in range(size)]
    visual(arr)
    if gamemode == 0:
        for hod in range(size ** 2):
            arr, last = human_turn(hod, arr, win)
            if not (arr != 0):
                return 0
    elif gamemode == 1:
        last = []
        for hod in range(size ** 2):
            arr, last = animal_turn(hod, arr, win, last)
            time.sleep(0.1)
            if not (arr != 0):
                return 0
    elif gamemode == 2:
        last = []
        for hod in range(size ** 2):
            if hod % 2 == 0:
                arr, last = animal_turn(hod, arr, win, last)
                if not (arr != 0):
                    return 0
            else:
                arr, last = human_turn(hod, arr, win)
                if not (arr != 0):
                    return 0
    print("Nichya.")


game(read_start())
# game([3, 3, 0])
