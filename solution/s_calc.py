def calcpath(data, row, i, ways):
    #     a=[1,-1]
    data[row][i] = 3  # 这里置为3表示已经这个点已经走过

    if row + 1 < len(data) and data[row + 1][i] == 2:  # 下一行
        if not calcpath(data, row + 1, i, ways):
            data[row + 1][i] = 2

    if row - 1 > -1 and data[row - 1][i] == 2:  # 上一行
        if not calcpath(data, row - 1, i, ways):
            data[row - 1][i] = 2

    if i + 1 < len(data[0]) and data[row][i + 1] == 2:  # 右一格
        if not calcpath(data, row, i + 1, ways):
            data[row][i + 1] = 2

    if i - 1 > -1 and data[row][i - 1] == 2:    # 左一格
        if not calcpath(data, row, i - 1, ways):
            data[row][i - 1] = 2
    for row1 in data:
        for i1 in row1:
            if i1 == 2:
                return False
    ways.append((row, i))
    return True
