#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'

import os

# ═══════════════════════════════════════════════
if os.name == 'nt':
    FONT_ROOT = 'D:/References/Fonts/Chinese/All/'
else:
    FONT_ROOT = '/Users/erimus/OneDrive/21MoSeeker/01公用素材/font'
PINGFANG = os.path.join(FONT_ROOT, 'PingFang.ttc')
SOURCE_HAN = os.path.join(FONT_ROOT, 'SourceHanSans 思源黑体 2.002.ttc')
MSYH = os.path.join(FONT_ROOT, '微软雅黑/msyh.ttc')
# ═══════════════════════════════════════════════
HERE = os.path.abspath(os.path.dirname(__file__))
# ═══════════════════════════════════════════════


def text2ucode(text): return hex(ord(text))[2:]
def ucode2text(ucode): return chr(int(f'0x{ucode}', 16))


def common_character():
    with open(os.path.join(HERE, 'data/常用汉字一级字表.txt'), 'r', encoding='utf-8') as f:
        common_character_list = [i.split(' ')[-1][0] for i in f.readlines()]
    return common_character_list


def list2excel(L):
    excel = ''
    for row in L:
        excel += ('\t'.join([str(i).replace('\t', ' ').replace('\n', ' ')
                             for i in row]) + '\n')
    with open(os.path.join(HERE, 'diff.csv'), 'w', encoding='utf-8') as f:
        f.write(excel)
    return excel
