from EasyClipToolMainFrame import *

if __name__ == '__main__':
    App = wx.App()
    mainFrame = EasyClipToolMainFrame(debug_log_level=3)
    mainFrame.Show(True)
    App.MainLoop()

    exit()
