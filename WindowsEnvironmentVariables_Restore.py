# Script Developer: Gabriel Mihai Sandu
# GitHub Profile: https://github.com/Gabrieliam42

import os
import sys
import ctypes
import subprocess

def check_admin_privileges():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin(script, params):
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)

def import_env_registry():
    cwd = os.getcwd()
    system_backup_path = os.path.join(cwd, 'env_system_backup.reg')
    user_backup_path = os.path.join(cwd, 'env_user_backup.reg')

    commands = [
        f'reg import "{system_backup_path}"',
        f'reg import "{user_backup_path}"'
    ]

    for cmd in commands:
        subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    if check_admin_privileges():
        import_env_registry()
    else:
        print("Script is not running with admin privileges. Restarting with admin privileges...")
        run_as_admin(os.path.abspath(__file__), "")
