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
import wx.lib.agw.aui as aui
import wx.lib.agw.fourwaysplitter as FWS

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
        # sizer = wx.BoxSizer(wx.HORIZONTAL)
        #
        # self.editor = md_editor.MarkdownEditor(self)
        # self.editor.Enable(False)
        # sizer.Add(self.editor, 1, wx.EXPAND)
        #
        # self.webview = webview.WebView.New(self)
        # sizer.Add(self.webview, 1, wx.EXPAND)
        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(self)

        # 创建工具栏
        self.toolbar = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                                      agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)

        self.mgr.AddPane(self.toolbar, aui.AuiPaneInfo().Name("toolbar").ToolbarPane().Top())

        # 创建内容区
        self.cPanel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 创建编辑区
        self.editor = md_editor.MarkdownEditor(self.cPanel)
        sizer.Add(self.editor, 1, wx.EXPAND)

        # 创建显示区
        self.webview = webview.WebView.New(self.cPanel)
        sizer.Add(self.webview, 1, wx.EXPAND)

        self.cPanel.SetSizer(sizer)
        self.cPanel.AutoLayout = True

        self.mgr.AddPane(self.cPanel, aui.AuiPaneInfo().Name("content").Center())

        self.mgr.Update()

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

    # --------------------------------------------------------------------------------
    def test(self):
        # print(self.mgr.SavePerspective())
        # pane = self.mgr.GetPaneByName("editer")
        # print(dir(pane))
        # pane.Hide()
        # self.mgr.SetDockSizeConstraint(0.5, 0.5)
        # self.mgr.Update()
        #print(dir(pane))
        self.editor.Show(False)
        self.cPanel.Layout()
