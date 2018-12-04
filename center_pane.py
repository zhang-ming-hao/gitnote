#!/usr/bin/env python
# coding:utf-8

"""
基于Github的Markdown笔记本——中央窗口
"""

import os
import wx
import sys
import codecs
import wx.stc as stc
import wx.html2 as webview
from SuperMarkdown import SuperMarkdown

import md_editor


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

        # 初始化变量
        self.parent = parent
        self.notePath = ""

        # 绘制界面
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.editor = md_editor.MarkdownEditor(self)
        self.editor.Enable(False)
        sizer.Add(self.editor, 1, wx.EXPAND)

        self.webview = webview.WebView.New(self)
        sizer.Add(self.webview, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.Layout()

        # 绑定事件
        self.Bind(stc.EVT_STC_CHANGE, self.OnEditorChange)

    # --------------------------------------------------------------------------------
    def OpenNote(self, path):
        """
        打开笔记

        :param path: 笔记路径
        """

        self.notePath = path

        fp = codecs.open(path, "r", "utf-8")
        md = fp.read()
        fp.close()

        self.editor.SetValue(md)
        self.editor.Enable(True)

    # --------------------------------------------------------------------------------
    def OnEditorChange(self, evt):
        """
        编辑器文本变化事件处理

        :param evt: 事件参数
        """

        # 保存md
        md = self.editor.GetValue()
        fp = codecs.open(self.notePath, "w", "utf-8")
        fp.write(md)
        fp.close()

        # 编译为html并保存
        smd = SuperMarkdown.SuperMarkdown()
        smd.add_content(text=md)
        html = smd.build()
        htmlPath = os.path.join(os.path.split(self.notePath)[0], ".html")
        fp = codecs.open(htmlPath, "w", "utf-8")
        fp.write(html)
        fp.close()

        # 显示html内容
        root = os.path.split(sys.argv[0])[0]
        self.webview.LoadURL(os.path.join(root, htmlPath))
