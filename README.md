# gitnote
利用Github制作的云笔记系统。
本系统使用python3.7开发，主架构采用wxPython，并在wxPython中嵌入CEFPython3，使用HTML+CSS+JS进行前端开发。
使用editor.md作为MarkDown编辑器。

感谢上述开源项目的开发者。

## 打包说明
本项目使用的python版本为3.7，pyinstaller版本为3.4
可使用如下命令进行打包：
```
pyinstaller GitNote.spec
```
