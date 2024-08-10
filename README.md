# Easy Clip Tool
***一款简单的影视素材剪辑器***

---

## 什么是 Easy Clip Tool
Easy Clip Tool 是一款简单的影视素材剪辑器，它可以对素材（建议是尺寸相似的）进行简单剪辑，
例如调整顺序，截取其中某一个片段。

制作它的灵感和需求来源于对游戏即时回放片段的拼接，通过它您可以轻松的对各种即时回放片段进行拼接和简单处理。

它的工作原理很简单：将界面上设置的参数转化为使用 ffmpeg 进行处理的命令行，然后自动调用ffmpeg对素材进行处理。

## 我该如何获取 Easy Clip Tool
获取 Easy Clip Tool，可以在 release 页面中找到打包可供 windows 平台使用的可执行程序文件。

对于其他平台，很不幸的是，您可能需要下载项目源代码进行一些修改——因为我在命令行生成的部分以 windows 平台为目标实现了。
关于命令行生成的部分，您可以在 (`EasyClipMainFrame.py`) `PureClipMainFrame.ExportBtnOnClick()` 的实现中找到。

---

## 如何使用项目源代码
项目源代码由四个文件组成：

- `main.py`
- `PureClip.py`
- `PureClipMainFrame.py`
- `PureClipFBP.fbp`

我会在下面一个接一个地介绍这些文件的作用。
### `main.py`
这是整个程序的入口文件，如果想要直接在python中运行整个程序，请直接运行这个文件

### `EasyClipTool.py`
这是由 wxFormBuilder 生成的文件，主要对程序界面和控件进行了布局并绑定了相关的回调函数。

不建议修改它。

### `EasyClipToolMainFrame.py`
这是程序主要逻辑实现的地方。

### `EasyClipToolFBP.fbp`
这是 wxFormBuilder 的工程文件，使用 wxFormBuilder 打开这个工程文件，您可以看到这个程序的界面设计。