#!/usr/bin/env python
# coding:utf-8

"""
响应js与python的交互，对数据进行处理
"""

import os
import wx
import codecs


class MDBox:
    """
    Markdown数据处理类，需要JS端调用
    """

    def __init__(self, mdpath):
        """
        构造函数

        Args:
            mdpath: 文件夹路径或文件路径
        """

        self.mdpath = mdpath
        self.notedir = "note"

    def GetList(self, dir, callback):
        """
        取得目录下的文件和文件夹列表

        Args:
            dir: 目录
            callback: 回调函数
        """

        if len(dir) == 0:
            dir = self.notedir

        folders = []
        notes = []
        fl = os.listdir(dir)
        for f in fl:
            fpath = os.path.join(dir, f)
            if os.path.isdir(fpath):
                # 每个笔记均是一个目录， 目录中包含一个与目录同名的md文件，和一个res目录用来保存图片
                mdpath = os.path.join(fpath, f"{f}.md")

                # 判断目录中是否有与目录同名的md文件
                if os.path.isfile(mdpath):
                    notes.append({"name": f, "path": mdpath})
                else:
                    folders.append({"name": f, "path": fpath})

        callback.Call(folders, notes)

    def SetCurrent(self, mdpath):
        """
        设置当前文件
        Args:
            mdpath: 文件路径
        """

        self.mdpath = mdpath

    def GetContent(self, callback):
        """
        取得文件内容

        Args:
            callback: js的回调函数
        """

        if self.mdpath:
            with codecs.open(self.mdpath, 'r', 'utf-8') as fp:
                callback.Call(fp.read())
        else:
            callback.Call("")

    def GetTitle(self, callback):
        """
        取得文件标题

        Args:
            callback: 回调函数
        """

        fname = os.path.basename(self.mdpath)
        title = os.path.splitext(fname)[0]
        callback.Call(title)

    def SaveContent(self, content):
        """
        保存文件内容

        Args:
            content: 内容
        """

        if self.mdpath:
            with codecs.open(self.mdpath, 'w', 'utf-8') as fp:
                fp.write(content)
