#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

from PIL import Image, ImageFont, ImageDraw
from config import *

# ═══════════════════════════════════════════════
here = os.path.abspath(os.path.dirname(__file__))
# ═══════════════════════════════════════════════

'''
把文字存为图片
大部分字体vertical height（不等于行高）大于宽度，
所以要先贴到长方形的图里，再切掉上下多余的部分。
'''


def character_to_image(text, path='', size=16,
                       font=None,         # 批量处理时直接传入font避免重复解析
                       font_file=None,    # 字体文件
                       index=0,           # 字体序号
                       return_data=False):
    ucode = hex(ord(text))[2:]
    # text = chr(int(f'0x{ucode}', 16))
    im = Image.new("L", (size, size * 2), (255))  # 预留两倍行高
    dr = ImageDraw.Draw(im)
    if font is None:
        font = ImageFont.truetype(font_file, size, index=index)

    dr.text((0, 0), text, font=font, fill="#000000")
    top = int(size * 0.3)  # 根据思源调整的参数
    im = im.crop((0, top, size, top + size))  # l,t,r,b
    # im.show()
    # return

    if return_data:
        return im
    else:
        # 保存图片文件
        im.save(os.path.join(path, 'img', f"{ucode}_{text}_{index:02d}.png"))


# 取数据画成图
def draw_img_by_array(data):
    edge = int(len(data)**0.5)
    im = Image.new("L", (edge, edge), (255))
    pim = im.load()
    for y in range(edge):
        for x in range(edge):
            pim[x, y] = data[x + y * edge]
    # im.show()
    im.save(os.path.join(here, 'img', f"{timestamp()}.png"))


# 用思源黑体绘制常用汉字
def draw_common_character_with_source_sans():
    font_dict = {}
    size = 64
    for index, name in sourcesans_dict.items():
        font = ImageFont.truetype(SOURCE_HAN, size, index=index)
        font_dict[index] = font

    with open(os.path.join(here, 'data/常用汉字一级字表.txt'), 'r', encoding='utf-8') as f:
        for i in f.readlines():
            text = i.split(' ')[-1][0]
            print(f'{text = }')
            for index, font in font_dict.items():
                character_to_image(text, path=here, size=size,
                                   font=font, index=index)


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    text = '亲'
    text = '靇'

    sourcesans_dict = {
        25: "SourceHanSans-Regular",
        26: "SourceHanSansK-Regular",
        27: "SourceHanSansSC-Regular",
        28: "SourceHanSansTC-Regular",
        29: "SourceHanSansHC-Regular",
    }

    for index, name in sourcesans_dict.items():
        size = 64
        font = ImageFont.truetype(SOURCE_HAN, size, index=index)
        character_to_image(text, path=here, size=size, font=font)

    # draw_common_character_with_source_sans()
