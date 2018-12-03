#!/usr/bin/env python
# coding:utf-8

"""
基于Github的Markdown笔记本主程序
"""

import os
import wx
import wx.lib.agw.aui as aui

APP_TITLE = "Git Note"


# ================================================================================
class MainFrame(wx.Frame):
    """
    主框架
    """

    # --------------------------------------------------------------------------------
    def __init__(self, parent=None):
        """
        MainFrame的构造函数

        :param parent: 父窗口，如果为None则默认为桌面
        """

        wx.Frame.__init__(self, parent, -1, APP_TITLE, style=wx.DEFAULT_FRAME_STYLE)
        self.Maximize()

