#!/usr/bin/env python
# coding:utf-8

"""
利用Github制作的云笔记系统。
本系统使用python3.7开发，主架构采用wxPython，并在wxPython中嵌入CEFPython3，使用HTML+CSS+JS进行前端开发。
使用editor.md作为MarkDown编辑器。

感谢上述开源项目的开发者。
"""

import os
import wx
import sys
from cefpython3 import cefpython as cef

import mdbox


class MainFrame(wx.Frame):
    """
    主框架
    """

    def __init__(self, filepath=""):
        """
        构造函数

        Args:
            filepath: 打开的文件路径
        """

        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title='GitNote')

        # 初始化变量
        self.dir = os.path.split(sys.argv[0])[0]

        # 加载图标
        self.SetIcon(wx.Icon(os.path.join(self.dir, "res", "images", "gitnote.ico"), wx.BITMAP_TYPE_ICO))

        # 窗口最大化
        self.Maximize()

        # 初始化浏览器
        cef.Initialize()

        wi = cef.WindowInfo()
        width, height = self.GetSize().Get()
        wi.SetAsChild(self.GetHandle(), [0, 0, width, height])
        self.browser = cef.CreateBrowserSync(wi)
        print(os.path.join(self.dir, "res", "html", "editor.html"))
        self.browser.LoadUrl(os.path.join(self.dir, "res", "html", "editor.html"))

        js = cef.JavascriptBindings()
        box = mdbox.MDBox(filepath)
        js.SetObject('mdbox', box)

        self.browser.SetJavascriptBindings(js)

        # 绑定事件
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

    def OnSetFocus(self, _):
        """
        取得焦点的事件处理
        """

        cef.WindowUtils.OnSetFocus(self.GetHandle(), 0, 0, 0)
        self.browser.SetFocus(True)

    def OnSize(self, _):
        """
        窗口大小改变事件处理
        """

        cef.WindowUtils.OnSize(self.GetHandle(), 0, 0, 0)
        self.browser.NotifyMoveOrResizeStarted()

    def OnClose(self, event):
        """
        窗口关闭事件处理

        Args:
            event: 事件参数
        """

        self.browser.ParentWindowWillClose()
        event.Skip()

    def OnIdle(self, _):
        """
        系统空转事件处理
        """

        cef.MessageLoopWork()


class MainApp(wx.App):
    """
    主应用程序
    """

    def OnInit(self):
        """
        主应用程序初始化回调函数
        :return: True
        """

        return True

    # --------------------------------------------------------------------------------
    def show_mainframe(self, filepath=""):
        """显示主框架

        Args:
            default_file: 默认文件
        """

        self.frame = MainFrame(filepath)
        self.frame.Show()


def main(filepath=""):
    """
    主函数
    """

    app = MainApp()
    app.show_mainframe(filepath)
    app.MainLoop()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
