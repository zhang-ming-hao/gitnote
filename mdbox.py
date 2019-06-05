#!/usr/bin/env python
# coding:utf-8

import codecs


class MDBox:
    """
    Markdown数据处理类，需要JS端调用
    """

    def __init__(self, mdpath):
        """
        构造函数

        Args:
            mdpath: 文件路径
        """

        self.mdpath = mdpath

    def get_content(self, callback):
        """
        取得文件内容

        Args:
            callback: js的回调函数
        """

        with codecs.open(self.mdpath, 'r', 'utf-8') as fp:
            callback.Call(fp.read())

    def save_content(self, content):
        """
        保存文件内容

        Args:
            content: 内容
        """

        with codecs.open(self.mdpath, 'w', 'utf-8') as fp:
            fp.write(content)
