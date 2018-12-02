from solution.s_calc import calcpath
from solution.s_img import Img


def p_f(data):
    ways = []
    for row in data:
        for column in row:
            if column == 0:
                calcpath(data, data.index(row), row.index(column), ways)  # x 3 0 ,[]
    return list(reversed(ways))


if __name__ == '__main__':
    img = Img('./a.jpg', 'a')
    img.cutimage()
    img.calccoordinates()
    result = p_f(img.result_lsit)
    img.mergeimage(result)
    print(result)
