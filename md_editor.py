#!/usr/bin/env python
# coding:utf-8

"""
Markdown文本编辑器
"""

import wx
import wx.stc as stc

faces = {'times': 'Times',
         'mono': 'Courier',
         'helv': 'Helvetica',
         'other': 'new century schoolbook',
         'size': 12,
         'size2': 10,
         }


# ================================================================================
class MarkdownEditor(stc.StyledTextCtrl):
    """
    Markdown文本编辑器
    """

    fold_symbols = 2

    def __init__(self, parent):
        """
        构造函数

        :param parent:   父窗口
        :param filePath: 文件路径
        """

        stc.StyledTextCtrl.__init__(self, parent, -1)

        # 设置记法分析程序
        self.SetLexer(stc.STC_LEX_MARKDOWN)

        # 设置按词语折行
        self.SetWrapMode(stc.STC_WRAP_WORD)

        # 显示行号
        self.SetMarginType(0, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(0, 20)

        # 设置字体字号
        self.StyleSetFont(0, wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑"))




