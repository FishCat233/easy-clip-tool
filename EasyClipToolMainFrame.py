"""Subclass of MainFrame, which is generated by wxFormBuilder."""
import os
import subprocess
import time
import webbrowser

import wx
import EasyClipTool


class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, mainframe):
        super().__init__()
        self.mainframe = mainframe

    def OnDropFiles(self, x, y, filenames):
        for filename in filenames:
            self.mainframe.add_files(self.mainframe.list_ctrl.GetItemCount(), os.path.basename(filename), filename)
        return True


# Implementing MainFrame
class EasyClipToolMainFrame(EasyClipTool.MainFrame):
    def __init__(self, parent=None, debug_log_level=0):
        EasyClipTool.MainFrame.__init__(self, parent)

        self.first_selected_index = 0
        self.debug_log_level = debug_log_level
        self.item_list = []  # 列表是控件上的映射，列表的物品顺序就是控件上物品的顺序

        # list_ctrl 控件添加列
        self.list_ctrl.InsertColumn(0, "序号", width=40)
        self.list_ctrl.InsertColumn(1, "文件名", width=280)
        self.list_ctrl.InsertColumn(2, "开始时间", width=65)
        self.list_ctrl.InsertColumn(3, "结束时间", width=65)
        self.list_ctrl.InsertColumn(4, "文件路径", width=238)

        # 绑定 drop file
        self.m_notebook1.SetDropTarget(MyFileDropTarget(self))

    # Handlers for MainFrame events.
    def ApplyTimeButtonOnClick(self, event):
        apply_time_item_index = self.first_selected_index

        # 从控件上读取时间
        start_time = self.StartTimeCtrl.GetValue()
        end_time = self.EndTimeCtrl.GetValue()

        # 一些提升体验的小更改
        # 将空格替换为 ":"
        start_time = str.replace(start_time, " ", ":")
        end_time = str.replace(end_time, " ", ":")
        # 将全角 “：” 替换为半角 “:”
        start_time = str.replace(start_time, "：", ":")
        end_time = str.replace(end_time, "：", ":")

        # 设置物品列表的参数，如果为空就不更改
        if not start_time == '':
            self.item_list[apply_time_item_index]["start_time"] = start_time
        if not end_time == '':
            self.item_list[apply_time_item_index]["end_time"] = end_time

        # 更新界面
        self.list_load_item(self.item_list[apply_time_item_index], apply_time_item_index)

    def AddFileBtnOnClick(self, event):
        # 文件选择对话框
        file_dlg = wx.FileDialog(self, u"选择导入的文件", "", "", "*.mp4", wx.FD_OPEN)
        if file_dlg.ShowModal() == wx.ID_OK:
            # 文件导入
            # {NO, filename, startTime, endTime, path}

            # 将导入文件数据转为字典
            item_no = self.list_ctrl.GetItemCount()
            filename = file_dlg.GetFilename()
            path = file_dlg.GetPath()

            # 更改: 使用 self.add_files()
            self.add_files(item_no, filename, path)

            if self.debug_log_level > 2:
                print("{}, {}".format(file_dlg.GetFilename(), file_dlg.GetPath()))

        file_dlg.Destroy()

    def list_ctrl_on_drop_files(self, event):
        files = event.GetFiles()

        # 防止拖空文件
        if len(files) <= 0:
            return

        if self.debug_log_level > 2:
            print(files)

        for filename in files:
            item_no = self.list_ctrl.GetItemCount()
            self.add_files(item_no, filename, filename)

    def RemoveBtnOnClick(self, event):
        # 删除列表中的项
        delete_index = self.first_selected_index

        try:
            self.item_list.pop(delete_index)
        except:
            wx.MessageBox("删除素材失败。", "错误", style=wx.YES_DEFAULT | wx.ICON_QUESTION)
            return

        # 删除界面中的项

        self.list_ctrl.DeleteItem(delete_index)

        # 删除以后进行序号重排
        for i in range(len(self.item_list)):
            if i < delete_index:
                continue

            # 从删除项以后的每一个项的序号都要 -1
            self.item_list[i]["no"] -= 1

            # 从删除项开始后面的每一个物品都重新加载
            self.list_load_item(self.item_list[i], i)

    def MovUpBtnOnClick(self, event):
        if self.first_selected_index == -1:
            return  # 如果没有选中

        if self.first_selected_index == 0:
            wx.MessageBox("选中素材已置顶。", "错误", style=wx.YES_DEFAULT | wx.ICON_QUESTION)
            return  # 如果是第一个物品

        self.item_swap(self.first_selected_index, self.first_selected_index - 1)

        self.list_ctrl.Select(self.first_selected_index, on=0)  # 取消原来的选中
        self.list_ctrl.Select(self.first_selected_index - 1)

    def MovDownBtnOnClick(self, event):
        if self.first_selected_index == -1:
            return  # 如果没有选中

        if self.first_selected_index == self.list_ctrl.GetItemCount() - 1:
            wx.MessageBox("选中素材在最末端。", "错误", style=wx.YES_DEFAULT | wx.ICON_QUESTION)
            return  # 如果是最后一个

        self.item_swap(self.first_selected_index, self.first_selected_index + 1)

        # 选中转移
        self.list_ctrl.Select(self.first_selected_index, on=0)  # 取消原来的选中
        self.list_ctrl.Select(self.first_selected_index + 1)

    def ExportBtnOnClick(self, event):
        # TODO: 加入x264对视频进行进一步压缩（可选“压缩”选项）

        # 从界面读取导出文件名、路径、码率
        export_name = self.ExportNameCtrl.GetValue()
        export_path = self.ExportPathCtrl.GetValue()
        export_mbps = self.ExportBitCtrl.GetValue()

        # 导出码率设置为空则使用 6 mbps
        if export_mbps == '':
            export_mbps = 6

        # 导出文件名为空则使用时间
        if export_name == '':
            export_name = str(time.strftime('No Title %Y.%m.%d - %H.%M.%S.output.mp4'))

        # 导出路径不为空则更改工作路径
        if not export_path == '':
            os.chdir(export_path)

        # 导出命令
        console_command = 'ffmpeg '
        filter_complex_param = ''
        last_no = 0

        for item in self.item_list:
            no = item["no"]
            start_time = item["start_time"]
            end_time = item["end_time"]
            item_path = item["path"]

            # 防止一些奇怪的东西
            if start_time == '':
                start_time = "开头"
            if end_time == '':
                end_time = "结尾"

            # 开始、结束时间以及路径的命令行参数生成
            if start_time == "开头":
                if end_time == "结尾":
                    template = f'-i "{item_path}" '
                else:
                    template = f'-to {end_time} -i "{item_path}" '
            elif end_time == "结尾":
                template = f'-ss {start_time} -i "{item_path}" '
            else:
                template = f'-ss {start_time} -to {end_time} -i "{item_path}" '

            console_command += template

            # -filter_complex 的参数生成
            filter_complex_param += f'[{no}:0] [{no}:1] '
            last_no = no

        # 如果只有一段素材，不使用 -filter_complex
        if not last_no == 0:
            # 多段素材，使用 -filter_complex
            # 拼接 -filter_complex 段
            filter_complex_text = (
                f'-filter_complex "{filter_complex_param}concat=n={last_no + 1}:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" ')

            console_command += filter_complex_text

        # 检查输出文件夹是否存在
        if not os.path.exists(r".\output"):
            os.makedirs("output")
        os.chdir("output")

        # 检查输出文件是否存在，如果存在就删除
        if os.path.exists(export_name):
            os.remove(export_name)

        # 拼接全指令
        console_command += fr'-b:v {export_mbps}M "{export_name}"'

        if self.debug_log_level > 0:
            print(console_command)

        # os.system 有坑
        # os.system(console_command)
        subprocess.check_call(console_command)

        os.chdir("..")
        return

    def ProjectWebBtnOnClick(self, event):
        """
        “访问项目”按钮
        :param event:
        :return:
        """
        webbrowser.open('https://github.com/FishCat233/easy-clip-tool')

    def add_files(self, item_no, filename, path):
        """
        添加文件。将文件添加到物品列表，并刷新显示在界面上
        :param item_no: 序号
        :param filename: 文件名
        :param path: 文件路径
        :return: 空
        """
        # 构建物品字典
        item_dict = {"no": item_no,
                     "filename": filename,
                     "start_time": "开头",
                     "end_time": "结尾",
                     "path": path
                     }

        # 加到物品表
        self.item_list.append(item_dict)

        # 显示数据在界面
        index = self.list_ctrl.InsertItem(item_dict["no"], item_dict["no"])
        self.list_load_item(item_dict, index)

        pass

    def list_ctrl_on_selected(self, event):
        self.first_selected_index = self.list_ctrl.GetFirstSelected()

        if self.debug_log_level > 3:
            print(
                f"Selected Item Index: {self.first_selected_index}, \
				Selected Item no: {self.item_list[self.first_selected_index]}")

    def item_swap(self, item1_index, item2_index):
        """
        交换物品函数。会交换物品在列表的序号，位置，并更新控件上的位置
        :param item1_index: 交换的物品 1
        :param item2_index: 交换的物品 2
        :return:
        """

        # 更新物品列表的序号
        temp = self.item_list[item1_index]["no"]
        self.item_list[item1_index]["no"] = self.item_list[item2_index]["no"]
        self.item_list[item2_index]["no"] = temp

        # 更新物品列表的位置
        temp = self.item_list[item1_index]
        self.item_list[item1_index] = self.item_list[item2_index]
        self.item_list[item2_index] = temp

        # 交换用户界面上的显示
        self.list_load_item(self.item_list[item1_index], self.item_list[item1_index]["no"])
        self.list_load_item(self.item_list[item2_index], self.item_list[item2_index]["no"])

    def list_load_item(self, load_item, list_ctrl_index):
        """
        把物品列表上的物品载入到用户界面的控件上
        :param load_item: 载入的物品
        :param list_ctrl_index: 载入在控件的行数
        :return: 无
        """
        self.list_ctrl.SetItem(list_ctrl_index, 0, str(load_item["no"]))
        self.list_ctrl.SetItem(list_ctrl_index, 1, load_item["filename"])
        self.list_ctrl.SetItem(list_ctrl_index, 2, load_item["start_time"])
        self.list_ctrl.SetItem(list_ctrl_index, 3, load_item["end_time"])
        self.list_ctrl.SetItem(list_ctrl_index, 4, load_item["path"])


if __name__ == '__main__':
    App = wx.App()
    mainFrame = EasyClipToolMainFrame(None)
    mainFrame.Show(True)
    App.MainLoop()
