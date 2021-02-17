#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
'''
读取字体信息。主要是index和对应的字体名。
ttc字体含多个字体，需要识别包含的字体。

读取字体文件内所包含的字符。
比较不同的字体文件所包含的字符差异。
'''

from fontTools.ttLib import TTFont, TTLibError
from .config import *

# ═══════════════════════════════════════════════


# 打印字体文件 ttc 所含的字体名称
def show_font_info(font_file):
    for fontNumber in range(99):
        try:
            print(f'\nOpen font index: {fontNumber}')
            with TTFont(font_file, fontNumber=fontNumber) as font:
                for i, record in enumerate(font['name'].names):
                    # print(f'{i:>2d} | {record}')  # 打印全部名称

                    # Source Han Sans 专用名称过滤器
                    rs = record.string
                    if all((len(rs) >= 16,  # b'\x00S' 13*2 个字符
                            b' ' not in rs,
                            b';' not in rs,
                            b'-' in rs
                            )):
                        # print(rs)
                        print(f'=== {record}')
        except Exception as e:
            print(repr(e))
            if type(e) == TTLibError:
                print(f'Total font number: {fontNumber}')
                return


# 列出字体文件所含全部字符
def list_all_glyph_in_font(font_file, font_index=0):
    print(f'Reading: {font_file} | {font_index}')
    font = TTFont(font_file, fontNumber=font_index)
    r = []
    for table in font['cmap'].tables:
        for k, v in table.cmap.items():
            # k: unicode10进制编码, 即 &#20648;
            # v: cid 意义不明
            # chr(k) unicode转实际字符 汉字
            r.append(chr(k))

    print(f'Total: {len(r)}')
    return r


# 检测字体是否包含常用汉字
def if_font_contain_common_character(font_file, font_index=0):
    all_character = list_all_glyph_in_font(font_file, font_index)
    here = os.path.abspath(os.path.dirname(__file__))
    file = os.path.join(here, 'data/常用汉字一级字表.txt')
    with open(file, 'r', encoding='utf-8') as f:
        common = [i.strip().split(' ')[-1][0]
                  for i in f.readlines() if i.strip()]
    print(f'Check if Character in Font\n{font_file} | {font_index=}')
    for i, c in enumerate(common):
        if c not in all_character:
            print(i, c)
            break
    else:
        print('All character in font!\n')


# 获取多个字体所含字符的交集
def get_same_glyph_in_multi_fonts(font_list):
    glyph_list = []  # 包含各个字体的字符集 [set(font1), set(font2), ...]
    for font, index in font_list:
        font = TTFont(font, fontNumber=index)
        glyph_set = []  # 当前字体的字符集
        for table in font['cmap'].tables:
            glyph_set += list(table.cmap.keys())  # keys 是unicode对应的十进制码
        glyph_list.append(set(glyph_set))

    result = None
    for gliyph_set in glyph_list:
        print(len(gliyph_set))
        if result is None:
            result = gliyph_set
        else:
            result = result & gliyph_set
    print(len(result))
    return result


# ═══════════════════════════════════════════════


if __name__ == '__main__':

    # 思源有45个字体，具体这个数字的来源还不知道怎么判断。
    # 直接用 font = TTFont(font) 返回的出错信息里会含有index数
    # 思源 27:SC, 28:TC, 29:HC
    show_font_info(SOURCE_HAN)
    # show_font_info(PINGFANG)

    # all_character = list_all_glyph_in_font(SOURCE_HAN)

    for index in {
        25: "SourceHanSans-Regular",
        26: "SourceHanSansK-Regular",
        27: "SourceHanSansSC-Regular",
        28: "SourceHanSansTC-Regular",
        29: "SourceHanSansHC-Regular",
    }:
        # if_font_contain_common_character(SOURCE_HAN, index)
        pass

    # result = get_same_glyph_in_fonts()
    # add_character_data_to_db(result)
