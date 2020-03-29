import keyboard,time,win32gui,win32con,os,subprocess


def enumHandler(hwnd, lParam):
    if win32gui.IsWindowVisible(hwnd):
        if 'SERVER' in win32gui.GetWindowText(hwnd):
            win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)


while True:
	keyboard.wait("F2")
	win32gui.EnumWindows(enumHandler, None)
	time.sleep(0.5)
	#subprocess.call(["RUN.bat"])
	p = subprocess.Popen('RUN.bat', creationflags=subprocess.CREATE_NEW_CONSOLE)

