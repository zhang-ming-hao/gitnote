#!/usr/bin/env python
# coding:utf-8

"""
基于Github的Markdown笔记本——主程序
"""

import os
import wx
import wx.lib.agw.aui as aui

import left_pane
import center_pane

APP_TITLE = "Git Note"


# ================================================================================
class MainFrame(wx.Frame):
    """
    主框架
    """

    DIR_RES  = "res"
    DIR_NOTE = "notes"

    # --------------------------------------------------------------------------------
    def __init__(self, parent=None):
        """
        MainFrame的构造函数

        :param parent: 父窗口，如果为None则默认为桌面
        """

        wx.Frame.__init__(self, parent, -1, APP_TITLE, style=wx.DEFAULT_FRAME_STYLE)
        self.Maximize()

        # 初始化目录
        if not os.path.isdir(self.DIR_NOTE):
            os.makedirs(self.DIR_NOTE)

        # 主框架布局
        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(self)

        # 创建左侧窗口
        self.leftPane = self._CreateLeftPane()

        # 创建中央窗口
        self.centerPane = self._CreateCenterPane()

        self.mgr.Update()

    # --------------------------------------------------------------------------------
    def _CreateLeftPane(self):
        """
        生成左侧窗口

        :return:  右侧窗口对象
        """

        leftPane = left_pane.LeftPane(self)
        self.mgr.AddPane(leftPane, aui.AuiPaneInfo().Name("left pane").Left().Caption("笔记目录").
                         Position(1).MinimizeButton(True).CloseButton(False).MinSize((320, -1)))

        return leftPane

    # --------------------------------------------------------------------------------
    def _CreateCenterPane(self):
        """
        生成中央窗口

        :return: 中央窗口对象
        """

        centerPane = center_pane.CenterPane(self)
        self.mgr.AddPane(centerPane, aui.AuiPaneInfo().Name("center pane").Center().Caption("笔记内容").
                         Position(1).MinimizeButton(False).CloseButton(False).MinSize((320, -1)))

        return centerPane


# ================================================================================
class MainApp(wx.App):
    """
    主应用程序
    """

    def OnInit(self):
        """
        主应用程序初始化回调函数
        :return: True
        """

        self.SetAppName(APP_TITLE)
        frame = MainFrame(None)
        frame.Show()

        return True

    # --------------------------------------------------------------------------------
    @staticmethod
    def ShowMessage(parent, message, button=wx.OK, icon=wx.ICON_ERROR):
        """
        显示消息

        :param parent:  父窗口
        :param message: 消息内容
        :param button:  显示按钮
        :param icon:    显示图标
        """

        dlg = wx.MessageDialog(parent, message, "提示", style=button | icon)
        ret = dlg.ShowModal()
        dlg.Destroy()

        return ret


# ----------------------------------------------------------------------
def main(debug=True):
    if debug:
        fp = open("debug.txt", "w")
        fp.close()
        app = MainApp(redirect=True, filename="debug.txt")
    else:
        app = MainApp()

    app.MainLoop()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
    main(False)
