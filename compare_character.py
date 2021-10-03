#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 比较思源黑体各地区字体的字型差异

import numpy as np
from character_to_image import character_to_image, ImageFont
from config import *

# ═══════════════════════════════════════════════
here = os.path.abspath(os.path.dirname(__file__))
# ═══════════════════════════════════════════════


def find_difference(text, size, font_list):
    data_list = None  # nparray 行：图，列：像素
    # 读取同一个字的所有图片的数据
    for i, font in enumerate(font_list):
        im = character_to_image(text, path=here, size=size,
                                font=font, return_data=True)
        img_data = np.asarray(im.getdata())
        if data_list is None:
            data_list = img_data
        else:
            data_list = np.vstack((data_list, img_data))
    # print(f'{data_list = }')

    # 比较各像素点的差异
    # print(f'{img_data_len = }')
    diff = []  # 所有数据的平均差记录容器
    medians = np.zeros(data_list.shape[1])
    for col in range(data_list.shape[1]):  # 按列读取
        this_pixel_datas = data_list[:, col]
        # print(f'{this_pixel_datas = }')
        this_pixel_stand = np.std(this_pixel_datas)  # 标准差
        diff.append(this_pixel_stand)

        medians[col] = np.median(this_pixel_datas)  # 获取中位数 比较各字型的偏差

    # diff_list 各字体的list和平均(中间)值的差异 用来表示哪个字型差异较大
    diff_list = abs(data_list - medians) / 255  # 行：图，列：像素
    # 取各字体的图的各像素和中间值的差异，取平均，表示和[大众]的区别程度
    diff_list = [f'{np.mean(img_diff):.3f}' for img_diff in diff_list]

    diff = np.mean(diff)  # 各像素点标准差的平均数 表示各字体的整体差异情况
    # print(f'{text}: {diff}')

    # 导出格式为excel 字（含字体），差异量
    row = [text, f'{diff:.2f}'] + diff_list
    # print(f'{row = }')
    return row


# ═══════════════════════════════════════════════
if __name__ == '__main__':

    sourcesans_dict = {
        25: "SourceHanSans-Regular",
        26: "SourceHanSansK-Regular",
        27: "SourceHanSansSC-Regular",
        28: "SourceHanSansTC-Regular",
        29: "SourceHanSansHC-Regular",
    }

    size = 64
    font_list = []
    for index in sourcesans_dict:
        font = ImageFont.truetype(SOURCE_HAN, size, index=index)
        font_list.append(font)

    excel = []
    for text in common_character():
        row = find_difference(text, size, font_list)
        excel.append(row)
        # break
    list2excel(excel)
