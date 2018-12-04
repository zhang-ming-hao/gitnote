#!/usr/bin/env python
# coding:utf-8

"""
基于Github的Markdown笔记本——左侧窗口
"""

import os
import wx
import shutil
import wx.lib.buttons as buttons


# ================================================================================
class LeftPane(wx.Panel):
    """
    左侧窗口
    """

    ID_NEW_DIR  = wx.NewIdRef()     # 新建目录
    ID_NEW_NOTE = wx.NewIdRef()     # 新建笔记
    ID_DELETE   = wx.NewIdRef()     # 删除文件夹或笔记
    ID_RENAME   = wx.NewIdRef()     # 重命名文件夹或笔记

    # --------------------------------------------------------------------------------
    def __init__(self, parent):
        """
        LeftPane的构造函数

        :param parent: 父窗口
        """

        wx.Panel.__init__(self, parent)

        self.parent = parent

        # 初始化变量
        self.notesDir = self.parent.DIR_NOTE    # 笔记保存目录
        self.curItem  = None    # 当前节点

        # 绘制界面
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.githubBtn = buttons.GenButton(self, -1, "登陆Github")
        sizer.Add(self.githubBtn, 0, wx.ALIGN_RIGHT | wx.TOP | wx.RIGHT, 20)

        self.tree = wx.TreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS)
        sizer.Add(self.tree, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()

        # 初始化目录树
        self.il = wx.ImageList(16, 16)
        self.dirIcon = self.il.Add(wx.Bitmap(os.path.join(self.parent.DIR_RES, 'dir.png')))
        self.fileIcon = self.il.Add(wx.Bitmap(os.path.join(self.parent.DIR_RES, 'file.png')))

        self.tree.SetImageList(self.il)
        self.root = self.tree.AddRoot(u"我的笔记")
        self.tree.SetItemData(self.root, self.notesDir)
        self.tree.SetItemImage(self.root, self.dirIcon, wx.TreeItemIcon_Normal)

        # 绑定事件
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnTreeMenu, self.tree)
        self.tree.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit, self.tree)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelect, self.tree)

        self.Bind(wx.EVT_MENU, self.OnNewDir, id=self.ID_NEW_DIR)
        self.Bind(wx.EVT_MENU, self.OnNewNote, id=self.ID_NEW_NOTE)
        self.Bind(wx.EVT_MENU, self.OnRename, id=self.ID_RENAME)
        self.Bind(wx.EVT_MENU, self.OnDelte, id=self.ID_DELETE)

        # 显示第一层目录树
        self.ShowTree(self.root)

    # --------------------------------------------------------------------------------
    def ShowTree(self, item):
        """
        显示目录树，目录树在硬盘上有如下规则：
        1. 目录树的节点分为笔记目录和笔记两种；
        2. 笔记目录是一个文件夹，因为git不能上传空的文件夹，所以该文件夹中包含一个.dir的空文件
        3. 笔记其实也是一个文件夹，目录中包含一个.md文件，可能还会有.res文件夹

        :param item: 树节点
        """

        path = self.tree.GetItemData(item)

        # 遍历目录
        fl = os.listdir(path)
        for f in fl:
            if f.startswith("."):
                continue

            sPath = os.path.join(path, f)
            if self.IsNoteDir(sPath):
                # 添加目录
                newItem = self.tree.AppendItem(item, f)
                self.tree.SetItemData(newItem, sPath)
                self.tree.SetItemImage(newItem, self.dirIcon, wx.TreeItemIcon_Normal)
                self.tree.SetItemHasChildren(newItem)

            if self.IsNote(sPath):
                # 添加笔记
                newItem = self.tree.AppendItem(item, f)
                self.tree.SetItemData(newItem, sPath)
                self.tree.SetItemImage(newItem, self.fileIcon, wx.TreeItemIcon_Normal)

        self.tree.Expand(item)

    # --------------------------------------------------------------------------------
    @staticmethod
    def IsNoteDir(path):
        """
        判断路径是否为笔记目录

        :param path: 文件路径

        :return: 是返回True，否则返回False
        """

        return os.path.isfile(os.path.join(path, ".dir"))

    # --------------------------------------------------------------------------------
    @staticmethod
    def IsNote(path):
        """
        判断路径是否为笔记

        :param path: 文件路径

        :return: 是返回True，否则返回False
        """

        return os.path.isfile(os.path.join(path, ".md"))

    # --------------------------------------------------------------------------------
    def OnTreeMenu(self, evt):
        """
        在树上显示菜单事件

        :param evt: 事件参数
        """

        pt = evt.GetPosition()
        item = self.tree.HitTest(pt)[0]

        if item:
            self.curItem = item

            path = self.tree.GetItemData(item)
            menu = wx.Menu()

            hasItem = False
            if not self.IsNote(path):
                hasItem = True

                # 显示目录菜单
                menuItem = wx.MenuItem(menu, self.ID_NEW_DIR, "新建目录")
                bmp = wx.Bitmap(os.path.join(self.parent.DIR_RES, 'dir.png'))
                menuItem.SetBitmap(bmp)
                menu.Append(menuItem)

                menuItem = wx.MenuItem(menu, self.ID_NEW_NOTE, "新建笔记")
                bmp = wx.Bitmap(os.path.join(self.parent.DIR_RES, 'file.png'))
                menuItem.SetBitmap(bmp)
                menu.Append(menuItem)

            if item != self.root:
                if hasItem:
                    menu.AppendSeparator()

                menuItem = wx.MenuItem(menu, self.ID_RENAME, "重命名")
                # bmp = wx.Bitmap(os.path.join(self.parent.DIR_RES, 'file.png'))
                # menuItem.SetBitmap(bmp)
                menu.Append(menuItem)

                menuItem = wx.MenuItem(menu, self.ID_DELETE, "删除")
                # bmp = wx.Bitmap(os.path.join(self.parent.DIR_RES, 'file.png'))
                # menuItem.SetBitmap(bmp)
                menu.Append(menuItem)

            self.PopupMenu(menu)
            menu.Destroy()

    # --------------------------------------------------------------------------------
    def OnNewDir(self, evt):
        """
        新建目录事件处理

        :param evt: 事件参数
        """

        newItem = self.tree.AppendItem(self.curItem, "")
        self.tree.SetItemImage(newItem, self.dirIcon, wx.TreeItemIcon_Normal)

        self.tree.Expand(self.curItem)
        self.tree.EditLabel(newItem)

    # --------------------------------------------------------------------------------
    def OnNewNote(self, evt):
        """
        新建笔记事件处理

        :param evt: 事件参数
        """

        newItem = self.tree.AppendItem(self.curItem, "")
        self.tree.SetItemImage(newItem, self.fileIcon, wx.TreeItemIcon_Normal)

        self.tree.Expand(self.curItem)
        self.tree.EditLabel(newItem)

    # --------------------------------------------------------------------------------
    def OnRename(self, evt):
        """
        重命名

        :param evt: 事件参数
        """

        self.tree.EditLabel(self.curItem)

    # --------------------------------------------------------------------------------
    def OnEndEdit(self, evt):
        """
        编辑结束事件处理

        :param evt:  事件参数
        """

        item = evt.GetItem()
        name = evt.GetLabel()

        # 名称非空检查
        if len(name) == 0:
            self.tree.EditLabel(item)

            return

        # 路径处理
        parent = self.tree.GetItemParent(item)
        pPath = self.tree.GetItemData(parent)
        path = os.path.join(pPath, name)
        oPath = self.tree.GetItemData(item)

        if path == oPath:
            return

        if os.path.isdir(path):
            # 目录已经存在
            wx.GetApp().ShowMessage(self, "指定的名称已存在。")
            self.tree.EditLabel(item)

            return

        if self.tree.GetItemImage(item) == self.dirIcon:
            # 处理目录

            if oPath:
                # 修改目录名
                os.rename(oPath, path)
            else:
                # 新建目录
                os.makedirs(path)
                fp = open(os.path.join(path, ".dir"), "w")
                fp.close()

            self.tree.SetItemData(item, path)
        else:
            # 处理笔记
            if oPath:
                # 修改笔记名
                os.rename(oPath, path)
            else:
                # 新建笔记
                os.makedirs(path)
                mdPath = os.path.join(path, ".md")
                fp = open(mdPath, "w")
                fp.close()

                self.parent.centerPane.OpenNote(mdPath)

            self.tree.SetItemData(item, path)

    # --------------------------------------------------------------------------------
    def OnDelte(self, evt):
        """
        删除目录或笔记

        :param evt: 事件参数
        """

        path = self.tree.GetItemData(self.curItem)
        name = os.path.basename(path)
        ret = wx.GetApp().ShowMessage(self, f"您确实要删除{name}吗？", wx.YES_NO, wx.ICON_QUESTION)
        if ret == wx.ID_YES:
            shutil.rmtree(path)
            self.tree.Delete(self.curItem)
            self.curItem = self.root

    # --------------------------------------------------------------------------------
    def OnTreeSelect(self, evt):
        """
        树节点选择事件处理

        :param evt:  事件参数
        """

        item = evt.GetItem()
        path = self.tree.GetItemData(item)
        if self.IsNote(path):
            self.parent.centerPane.OpenNote(os.path.join(path, ".md"))
