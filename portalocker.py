__all__ = [
    "lock",
    "unlock",
    "LOCK_EX",
    "LOCK_SH",
    "LOCK_NB",
    "LockException",
    "ProcessLock",
]

import os
import platform
import subprocess
import json
from datetime import datetime


class LockException(Exception):
    # Error codes:
    LOCK_FAILED = 1


class ProcessLock:
    def __init__(self, lock_file_path):
        self.lock_file_path = lock_file_path
        self.pid = os.getpid()
        self.timestamp = datetime.now().isoformat()

    def is_process_running(self, pid):
        system = platform.system().lower()
        try:
            if system == 'windows':
                output = subprocess.check_output(['tasklist', '/FI', f'PID eq {pid}'], text=True)
                return str(pid) in output
            elif system in ['linux', 'darwin']:
                output = subprocess.check_output(['ps', '-p', str(pid)], text=True)
                return str(pid) in output
            else:
                return False
        except (subprocess.CalledProcessError, Exception):
            return False

    def check_and_remove_stale_lock(self):
        try:
            with open(self.lock_file_path, 'r') as f:
                lock_data = json.load(f)
                pid = lock_data.get('pid')
                if pid and not self.is_process_running(pid):
                    os.remove(self.lock_file_path)
                    return True
            return False
        except (json.JSONDecodeError, FileNotFoundError):
            return True

    def write_lock_info(self):
        lock_data = {
            'pid': self.pid,
            'timestamp': self.timestamp,
            'system': platform.system()
        }
        with open(self.lock_file_path, 'w') as f:
            json.dump(lock_data, f)


if os.name == 'nt':
    import win32con
    import win32file
    import pywintypes
    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    LOCK_SH = 0  # the default
    LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
    __overlapped = pywintypes.OVERLAPPED()
elif os.name == 'posix':
    import fcntl
    LOCK_EX = fcntl.LOCK_EX
    LOCK_SH = fcntl.LOCK_SH
    LOCK_NB = fcntl.LOCK_NB
else:
    raise RuntimeError  #, "PortaLocker only defined for nt and posix platforms"

if os.name == 'nt':

    def lock(file, flags):
        hfile = win32file._get_osfhandle(file.fileno())
        try:
            win32file.LockFileEx(hfile, flags, 0, -0x10000, __overlapped)
        except pywintypes.error as exc_value:
            raise IOError

    def unlock(file):
        hfile = win32file._get_osfhandle(file.fileno())
        try:
            win32file.UnlockFileEx(hfile, 0, -0x10000, __overlapped)
        except pywintypes.error as exc_value:
            if exc_value[0] == 158:
                pass
            else:
                raise

elif os.name == 'posix':

    def lock(file, flags):
        try:
            fcntl.flock(file.fileno(), flags)
        except IOError as exc_value:
            raise IOError

    def unlock(file):
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)

if __name__ == "__main__":
    print(os.name)