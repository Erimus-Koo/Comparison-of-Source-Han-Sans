#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 比较思源黑体当前和之前版本的字型差异

import numpy as np
import cv2
import pandas as pd
import re
import imageio
from character_to_image import character_to_image, ImageFont
from compare_character import find_difference
from config import *

# ═══════════════════════════════════════════════
here = os.path.abspath(os.path.dirname(__file__))

SOURCE_HAN_PREV = os.path.join(FONT_ROOT,
                               'SourceHanSans 思源黑体 2.003.ttc')
versions = [SOURCE_HAN, SOURCE_HAN_PREV]
ver_list = sorted([re.findall(r'\d+\.\d+', v)[0] for v in versions])

sourcesans_dict = {
    # 25: "SourceHanSans-Regular",
    # 26: "SourceHanSansK-Regular",
    # 27: "SourceHanSansSC-Regular",
    # 28: "SourceHanSansTC-Regular",
    29: "SourceHanSansHC-Regular",
}
# ═══════════════════════════════════════════════


class imshow():
    def __init__(self):
        self.window_num = 0
        self.window_width = 1000
        self.x_gap, self.y_gap = 20, 200
        self.x, self.y = self.x_gap, self.y_gap

    def show(self, img_data, window_name='', wait=False):
        '''
        打印并显示图片数据
        '''
        img_data = np.copy(img_data)

        # create window
        self.window_num += 1
        window_name = f'[{self.window_num}]{window_name}'
        print(f'{window_name = }')
        cv2.namedWindow(window_name)

        # calculate window position
        cv2.moveWindow(window_name, self.x, self.y)
        print('window position:', self.x, self.y)
        h, w = img_data.shape[:2]
        self.x += (w + self.x_gap)
        if self.x >= self.window_width:
            self.y += self.y_gap
            self.x_gap += 20
            self.x = self.x_gap

        # img_data[img_data < 0] = 0
        # img_data[img_data > 255] = 255
        # 将 最小值~最大值 变形为 0~255
        min_v, max_v = img_data.min(), img_data.max()
        img_data = (img_data - min_v) / (max_v - min_v) * 255

        # show data
        cv2.imshow(window_name, img_data.astype(np.uint8))
        if wait:
            cv2.waitKey()


im = imshow()


def compare_diff_version(size, output):
    ver_list = sorted([re.findall(r'\d+\.\d+', v)[0] for v in versions])
    for index in sourcesans_dict:
        font_list = []
        for font_family in versions:
            font = ImageFont.truetype(font_family, size, index=index)
            font_list.append(font)

        excel = []
        for text in common_character()[:100]:
            row = find_difference(text, size, font_list)
            print(f'{row = }')
            excel.append(row)  # text, diff 因为只有两个 中值差异永远相等
            # break

        df = pd.DataFrame(excel, columns=['glyph', 'diff'] + ver_list)
        df.to_excel(output, index=False)


def draw_image(excel_file, size, w, h, output):
    # read excel, and pick up the most diff 100
    df = pd.read_excel(excel_file)
    df = df.sort_values('diff', ascending=False).head(w * h)
    print(f'{df = }')

    frames = []
    for vi, font_family in enumerate(versions):
        # create an empty canvas
        r = np.zeros((size * h + size, size * w, 3), np.uint8)
        for index in sourcesans_dict:
            font = ImageFont.truetype(font_family, size, index=index)
            for i, glyph in enumerate(df.glyph):
                print(f'{glyph = }')
                img = character_to_image(glyph, path=here, size=size,
                                         font=font, return_data=True)
                img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
                # print(f'{img.shape = }')
                # im.show(img, wait=1)
                r[i // h * size:i // h * size + size,
                  i % w * size:i % w * size + size] = img
        frames.append(r)

        # add font family info
        color = [180, 180, 180]
        color[vi % 3] = 240
        r = cv2.rectangle(r, (0, size * h), (size * w, r.shape[0]), color, -1)
        r = cv2.putText(r, os.path.split(font_family)[-1],
                        (50, r.shape[0] - 50), 1,
                        2, (0, 0, 0), 1, cv2.LINE_AA)
        # im.show(r, wait=1)

    imageio.mimsave(output, frames, 'GIF', duration=1)


# ═══════════════════════════════════════════════
if __name__ == '__main__':
    excel_output = os.path.join(here, f'version_diff_{"_".join(ver_list)}.xlsx')
    print(f'{excel_output = }')
    gif_output = os.path.join(here, f'version_diff_{"_".join(ver_list)}.gif')
    print(f'{gif_output = }')

    # 比较各版本的区别
    # compare_diff_version(size=64, output=excel_output)

    # 绘制不同字体
    draw_image(excel_file=excel_output, size=108, w=10, h=10, output=gif_output)
