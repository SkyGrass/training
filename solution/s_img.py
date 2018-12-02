from PIL import Image, ImageDraw, ImageFont
import colorsys
from collections import Counter
import os


class Img:
    img_name = ""
    img_obj = None
    img_size = None
    region = None
    region_list = []
    position_list = []
    position_rbg_list = []
    rgb_list = []
    cut_area = {'x': 0, 'y': 0, 'w': 0, 'h': 0}
    img = {'w': 0, 'h': 0}
    offset = {'w': 0, 'h': 0}
    target = {'w': 0, 'h': 0}
    x_max_count = 0
    y_max_count = 0
    result_lsit = []
    img_new_path = './cut//'  # 图片集地址
    img_format = ['.jpg', '.JPG']  # 图片格式
    img_new_size = 100  # 每张小图片的大小

    def __init__(self, imgpath, imgname):
        self.img_name = imgname
        self.img_obj = Image.open(imgpath)
        self.img_size = self.img_obj.size

    def cutimage(self):
        if self.img_size == (750, 1334):
            self.img.__setitem__('w', 100)
            self.img.__setitem__('h', 100)
            self.cut_area.__setitem__('x', 105)
            self.cut_area.__setitem__('y', 280)
            self.cut_area.__setitem__('w', 540)
            self.cut_area.__setitem__('h', 540)
            self.offset.__setitem__('w', 10)
            self.offset.__setitem__('h', 10)

            self.x_max_count = self.cut_area.get('w') // self.img.get('w')
            self.y_max_count = self.cut_area.get('h') // self.img.get('h')

            self.region = self.img_obj.crop((self.cut_area.get('x'), self.cut_area.get('y'),
                                             self.cut_area.get('w') + self.cut_area.get('x'),
                                             self.cut_area.get('h') + self.cut_area.get('y')))
            self.region.save('./' + self.img_name + '_cut' + '.jpg')
            self.img_obj = Image.open('./' + self.img_name + '_cut' + '.jpg')

            for x in range(self.x_max_count):
                self.target['h'] = x * self.img['h'] + x * self.offset['h']
                for y in range(self.y_max_count):
                    self.target['w'] = y * self.img['w'] + y * self.offset['w']
                    self.region = self.img_obj.crop((self.target['w'], self.target['h'],
                                                     self.img['w'] + self.target['w'],
                                                     self.img['h'] + self.target['h']))
                    self.region_list.append(self.region)
                    self.position_list.append((x, y))

                    rgb = (self.domaincolor(self.region))
                    self.position_rbg_list.append(rgb)
                    self.rgb_list.append(((x, y), rgb))

    def mergeimage(self, newlist):
        for (region, position) in zip(self.region_list, self.position_list):
            try:
                xh = str(newlist.index(position))
            except:
                xh = 'x'

            dr = ImageDraw.Draw(region)
            dr.text((40, 40), xh, (46, 139, 87))
            dr = ImageDraw.Draw(region)
            region.save('./cut/' + str(position) + '.jpg')

        image_names = [name for name in os.listdir(self.img_new_path) for item in self.img_format if
                       os.path.splitext(name)[1] == item]
        # 简单的对于参数的设定和实际图片集的大小进行数量判断
        if len(image_names) != self.x_max_count * self.y_max_count:
            raise ValueError("合成图片的参数和要求的数量不能匹配！")

        to_image = Image.new('RGB',
                             (self.x_max_count * self.img_new_size, self.y_max_count * self.img_new_size))  # 创建一个新图
        # 循环遍历，把每张图片按顺序粘贴到对应位置上
        for y in range(1, self.x_max_count + 1):
            for x in range(1, self.y_max_count + 1):
                from_image = Image.open(self.img_new_path + image_names[self.x_max_count * (y - 1) + x - 1]).resize(
                    (self.img_new_size, self.img_new_size), Image.ANTIALIAS)
                to_image.paste(from_image, ((x - 1) * self.img_new_size, (y - 1) * self.img_new_size))
        return to_image.save(self.img_name + '_new' + '.jpg')  # 保存新图

    def calccoordinates(self):
        clist = Counter(self.position_rbg_list)
        newlist = sorted(clist.items(), key=lambda x: x[1])
        newdic = dict(self.rgb_list)
        for x in range(self.x_max_count):
            _tt = []
            for y in range(self.y_max_count):
                newvalue = list(dict(newlist).keys()).index(newdic.__getitem__((x, y)))
                newdic.__setitem__((x, y), newvalue)
                _tt.append(newvalue)
            self.result_lsit.append(_tt)

    @staticmethod
    def domaincolor(image):
        image = image.convert('RGBA')

        # 生成缩略图，减少计算量，减小cpu压力
        image.thumbnail((200, 200))

        max_score = 0  # 原来的代码此处为None
        dominant_color = (0, 0, 0)  # 原来的代码此处为None，但运行出错，改为0以后运行成功，原因在于在下面的 score > max_score #的比较中，max_score的初始格式不定

        for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
            # 跳过纯黑色
            if a == 0:
                continue

            saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]

            y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)

            y = (y - 16.0) / (235 - 16)

            # 忽略高亮色
            if y > 0.9:
                continue

            # Calculate the score, preferring highly saturated colors.
            # Add 0.1 to the saturation so we don't completely ignore grayscale
            # colors by multiplying the count by zero, but still give them a low
            # weight.
            score = (saturation + 0.1) * count

            if score > max_score:
                max_score = score
                dominant_color = (r, g, b)

        return dominant_color
