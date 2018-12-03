#!/usr/bin/env python
# coding:utf-8

"""
基于Github的Markdown笔记本——中央窗口
"""

import os
import wx

# ================================================================================
class CenterPane(wx.Panel):
    """
    中央窗口
    """

    # --------------------------------------------------------------------------------
    def __init__(self, parent):
        """
        CenterPane的构造函数

        :param parent: 父窗口
        """

        wx.Panel.__init__(self, parent)

        self.parent = parent
