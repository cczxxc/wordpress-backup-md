---
id: 72
title: Python win32gui调用窗口到最前面
date: 2025-09-01T23:54:53
slug: python-win32gui调用窗口到最前面
original_slug: python-win32gui%e8%b0%83%e7%94%a8%e7%aa%97%e5%8f%a3%e5%88%b0%e6%9c%80%e5%89%8d%e9%9d%a2
link: https://xin.a0001.net/2025/09/01/python-win32gui%e8%b0%83%e7%94%a8%e7%aa%97%e5%8f%a3%e5%88%b0%e6%9c%80%e5%89%8d%e9%9d%a2/
status: publish
---

要写一个轮询几个重要页面的程序，不停的在大屏上进行刷新，通过pywin32模块下的SetForegroundWindow函数调用时，会出现error: (0, ‘SetForegroundWindow’, ‘No error message is available’)报错，后经网上查询确认，为pywin32模块下的一个小bug，在该函数调用前，需要先发送一个其他键给屏幕，如ALT键 。

对SetForegroundWindow进行重新封装以后的结果如下：

# Add this importimportwin32com.client  
# Add this to \_\_ini\_\_self.shell = win32com.client.Dispatch(“WScript.Shell”)  
# And SetAsForegroundWindow becomesdefSetAsForegroundWindow(self):  
    #发送ALT键，ALT键使用%号表示self.shell.SendKeys(‘%’)  
    win32gui.SetForegroundWindow(self.\_hwnd)

# coding: utf-8importre, traceback  
importwin32gui, win32con, win32com.client  
fromtime importsleep  
classcWindow:  
    def\_\_init\_\_(self):  
        self.\_hwnd = Noneself.shell = win32com.client.Dispatch(“WScript.Shell”)  
    defBringToTop(self):  
        win32gui.BringWindowToTop(self.\_hwnd)  
    defSetAsForegroundWindow(self):  
        self.shell.SendKeys(‘%’)  
        win32gui.SetForegroundWindow(self.\_hwnd)  
    defMaximize(self):  
        win32gui.ShowWindow(self.\_hwnd, win32con.SW\_MAXIMIZE)  
    defsetActWin(self):  
        win32gui.SetActiveWindow(self.\_hwnd)  
    def\_window\_enum\_callback(self, hwnd, wildcard):  
        ”’Pass to win32gui.EnumWindows() to check all the opened windows”’ifre.match(wildcard, str(win32gui.GetWindowText(hwnd))) isnotNone:  
            self.\_hwnd = hwnd  
    deffind\_window\_wildcard(self, wildcard):  
        self.\_hwnd = Nonewin32gui.EnumWindows(self.\_window\_enum\_callback, wildcard)  
    defkill\_task\_manager(self):  
        wildcard = ‘Gestionnaire des t.+ches de Windows’self.find\_window\_wildcard(wildcard)  
        ifself.\_hwnd:  
            win32gui.PostMessage(self.\_hwnd, win32con.WM\_CLOSE, 0, 0)  
            sleep(0.5)  
defmain():  
    sleep(5)  
    try:  
        wildcard = “.\*Building Operation WorkStation.\*”cW = cWindow()  
        cW.kill\_task\_manager()  
        cW.find\_window\_wildcard(wildcard)  
        cW.BringToTop()  
        cW.Maximize()  
        cW.SetAsForegroundWindow()  
    except:  
        f = open(“log.txt”, “w”)  
        f.write(traceback.format\_exc())  
        print(traceback.format\_exc())  
if\_\_name\_\_ == ‘\_\_main\_\_’:  
    main()

上面的操作已经很不错了，有人对此提出了更近一步的优化，表示在某此情况下，该脚本不能正常工作，又封装了两个函数，重新封装的类如下：

importwin32gui, win32con  
importre, traceback  
fromtime importsleep  
classcWindow:  
    def\_\_init\_\_(self):  
        self.\_hwnd = NonedefSetAsForegroundWindow(self):  
        # First, make sure all (other) always-on-top windows are hidden.self.hide\_always\_on\_top\_windows()  
        win32gui.SetForegroundWindow(self.\_hwnd)  
    defMaximize(self):  
        win32gui.ShowWindow(self.\_hwnd, win32con.SW\_MAXIMIZE)  
    def\_window\_enum\_callback(self, hwnd, regex):  
        ”’Pass to win32gui.EnumWindows() to check all open windows”’ifself.\_hwnd isNoneandre.match(regex, str(win32gui.GetWindowText(hwnd))) isnotNone:  
            self.\_hwnd = hwnd  
    deffind\_window\_regex(self, regex):  
        self.\_hwnd = Nonewin32gui.EnumWindows(self.\_window\_enum\_callback, regex)  
    defhide\_always\_on\_top\_windows(self):  
        win32gui.EnumWindows(self.\_window\_enum\_callback\_hide, None)  
    def\_window\_enum\_callback\_hide(self, hwnd, unused):  
        ifhwnd != self.\_hwnd: # ignore self# Is the window visible and marked as an always-on-top (topmost) window?ifwin32gui.IsWindowVisible(hwnd) andwin32gui.GetWindowLong(hwnd, win32con.GWL\_EXSTYLE) & win32con.WS\_EX\_TOPMOST:  
                # Ignore windows of class ‘Button’ (the Start button overlay) and# ‘Shell\_TrayWnd’ (the Task Bar).className = win32gui.GetClassName(hwnd)  
                ifnot(className == ‘Button’orclassName == ‘Shell\_TrayWnd’):  
                    # Force-minimize the window.# Fortunately, this seems to work even with windows that# have no Minimize button.# Note that if we tried to hide the window with SW\_HIDE,# it would disappear from the Task Bar as well.win32gui.ShowWindow(hwnd, win32con.SW\_FORCEMINIMIZE)  
defmain():  
    sleep(5)  
    try:  
        regex = “.\*Building Operation WorkStation.\*”cW = cWindow()  
        cW.find\_window\_regex(regex)  
        cW.Maximize()  
        cW.SetAsForegroundWindow()  
    except:  
        f = open(“log.txt”, “w”)  
        f.write(traceback.format\_exc())  
        print(traceback.format\_exc())  
main()
