import time
from pypresence import Presence

import win32gui
import win32process

import psutil
import ctypes

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

client_id = "928957672907227147"

def getProcessIDByName():
    qobuz_pids = []
    process_name = "Qobuz.exe"

    for proc in psutil.process_iter():
        if process_name in proc.name():
            qobuz_pids.append(proc.pid)

    return qobuz_pids

def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        #if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)

        if found_pid == pid:
            hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds 

def getWindowTitleByHandle(hwnd):
    length = GetWindowTextLength(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    return buff.value

def getQobuzHandle():
    pids = getProcessIDByName()

    for i in pids:
        hwnds = get_hwnds_for_pid(i)
        for hwnd in hwnds:
            if IsWindowVisible(hwnd):
                return hwnd


if __name__ == '__main__':
    qobuz_handle = getQobuzHandle()

    RPC = Presence(client_id)

    RPC.connect()

    title = ""

    while True:

        while True:
            new_title = getWindowTitleByHandle(qobuz_handle)

            if title != new_title:
                title = new_title
                break

        if title == 'Qobuz':
            print('resetting')
            RPC.clear()
        else:
            try:
                title_parts = title.split('-')
                print(title_parts)
                RPC.update(details=title_parts[0], state="by " + title_parts[1], large_image="qobuz")
            except:
                print("split not worked")
