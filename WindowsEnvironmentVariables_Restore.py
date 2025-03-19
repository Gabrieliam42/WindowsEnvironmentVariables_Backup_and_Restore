# Script Developer: Gabriel Mihai Sandu
# GitHub Profile: https://github.com/Gabrieliam42

import os
import winreg
import ctypes
import sys
import time
import json

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

def restore_environment_variables(file_path):
    with open(file_path, 'r') as file:
        env_vars = json.load(file)

    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0, winreg.KEY_ALL_ACCESS) as key:
        for name, value in env_vars["system"].items():
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_ALL_ACCESS) as key:
        for name, value in env_vars["user"].items():
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)

if __name__ == "__main__":
    if not is_admin():
        print("Requesting administrative privileges...")
        run_as_admin()
        sys.exit()

    file_path = "env_vars_backup.json"

    restore_environment_variables(file_path)
    print("Environment variables restored from backup.")
