import ctypes
from ctypes import Structure, byref, c_uint, sizeof, windll, wintypes
import os
import sys
import tempfile
from os.path import expanduser


class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ("ACLineStatus", wintypes.BYTE),
        ("BatteryFlag", wintypes.BYTE),
        ("BatteryLifePercent", wintypes.BYTE),
        ("Reserved1", wintypes.BYTE),
        ("BatteryLifeTime", wintypes.DWORD),
        ("BatteryFullLifeTime", wintypes.DWORD),
    ]


class LASTINPUTINFO(Structure):
    _fields_ = [
        ("cbSize", c_uint),
        ("dwTime", c_uint),
    ]


def get_ac_status():
    SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)
    GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
    GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
    GetSystemPowerStatus.restype = wintypes.BOOL

    status = SYSTEM_POWER_STATUS()
    if not GetSystemPowerStatus(ctypes.pointer(status)):
        raise ctypes.WinError()
    return status


def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0


def get_sys_folder(folder):
    if folder == "TEMP":
        return tempfile.gettempdir()
    elif folder == "HOME":
        return expanduser("~")
    else:
        return None


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_powershell_path():
    return "%SystemRoot%\system32\WindowsPowerShell\\v1.0\powershell.exe"


def is_admin():
    print("Checking if user is admin...")
    return ctypes.windll.shell32.IsUserAnAdmin() != 0
