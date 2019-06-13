#!/usr/bin/env python
# coding:utf-8

"""
响应js与python的交互，对数据进行处理
"""

import os
import wx
import codecs
import shutil


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

    def GetList(self, path, callback):
        """
        取得目录下的文件和文件夹列表

        Args:
            path: 文件夹相对路径
            callback: 回调函数
        """

        path = os.path.join(self.notedir, path)

        folders = []
        notes = []
        fl = os.listdir(path)
        for f in fl:
            fpath = os.path.join(path, f)
            if os.path.isdir(fpath):
                # 每个笔记均是一个目录， 目录中包含一个与目录同名的md文件，和一个res目录用来保存图片
                mdpath = os.path.join(fpath, f"{f}.md")

                # 判断目录中是否有与目录同名的md文件
                if os.path.isfile(mdpath):
                    notes.append(f)
                else:
                    folders.append(f)

        callback.Call(folders, notes)

    def SetCurrent(self, mdpath):
        """
        设置当前文件
        Args:
            mdpath: 文件路径
        """

        name = os.path.split(mdpath)[1]

        self.mdpath = os.path.join(self.notedir, mdpath, f"{name}.md")

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

    def AddFolder(self, path, callback):
        """
        新建文件夹

        Args:
            path: 文件夹相对路径
            callback: 回调函数
        """

        try:
            path = os.path.join(self.notedir, path)

            name = "新建文件夹"
            count = 0
            fl = os.listdir(path)
            for f in fl:
                if f.startswith(name):
                    count += 1

            if count:
                name += f"({count})"

            path = os.path.join(path, name)
            os.mkdir(path)

            callback.Call(name)
        except:
            pass

    def RenameFolder(self, path, newname, callback):
        """
        重命名文件夹

        Args:
            path: 文件夹相对路径
            newname:  新名称
            callback: 回调函数
        """

        try:
            path = os.path.join(self.notedir, path)

            dir = os.path.split(path)[0]
            dst = os.path.join(dir, newname)
            os.rename(path, dst)

            callback.Call(newname, True)
        except:
            callback.Call(newname, False)

    def AddNote(self, path, callback):
        """
        新建笔记

        Args:
            path: 文件夹相对路径
            callback: 回调函数
        """

        try:
            path = os.path.join(self.notedir, path)

            name = "新建笔记"
            count = 0
            fl = os.listdir(path)
            for f in fl:
                if f.startswith(name):
                    count += 1

            if count:
                name += f"({count})"

            path = os.path.join(path, name)
            os.mkdir(path)
            path = os.path.join(path, f"{name}.md")
            fp = open(path, "w")
            fp.close()

            callback.Call(name)
        except:
            pass

    def RenameNote(self, path, newname, callback):
        """
        重命名笔记

        Args:
            path: 笔记相对路径
            newname:  新名称
            callback: 回调函数
        """

        try:
            path = os.path.join(self.notedir, path)
            dir, name = os.path.split(path)

            # 先修改文件夹
            dst = os.path.join(dir, newname)
            os.rename(path, dst)

            # 再修改md文件
            path = os.path.join(dst, f"{name}.md")
            dst = os.path.join(dst, f"{newname}.md")
            os.rename(path, dst)

            callback.Call(newname, True)
        except:
            callback.Call(newname, False)

    def RemoveFolder(self, path, callback):
        """
        删除文件夹

        Args:
            path:     文件夹相对路径
            callback: 回调函数
        """

        try:
            path = os.path.join(self.notedir, path)
            shutil.rmtree(path)

            callback.Call()
        except:
            pass

    def RemoveNote(self, path, callback):
        """
        删除笔记

        Args:
            path:     笔记相对路径
            callback: 回调函数
        """

        try:
            path = os.path.join(self.notedir, path)
            shutil.rmtree(path)

            callback.Call()
        except:
            pass
