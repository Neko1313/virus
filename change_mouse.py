import os
import ctypes
import win32api
import win32con
from win32com.shell import shell, shellcon



class SystemChange:
    def __init__(self) -> None:
        self.replace_path = r"HKEY_CURRENT_USER\Control Panel\Cursors"
        self.location = os.path.dirname(os.path.realpath("__file__"))+"\media"
        self.user = ctypes.windll.user32

    def change_cursor(self):
        os.system(f"""REG ADD "{self.replace_path}" /v Arrow /t REG_EXPAND_SZ /d "{self.location}\cursor.cur" /f""")
        self.user.SystemParametersInfoA(0x57)

    def change_icons(self):  
        desktop_folder = shell.SHGetFolderPath(
        0, shellcon.CSIDL_DESKTOPDIRECTORY, 0, 0)

        # Обход всех папок на рабочем столе и замена иконок
        for folder_name in os.listdir(desktop_folder):
            folder_path = os.path.join(desktop_folder, folder_name)
            win32api.SetFileAttributes(folder_path,win32con.FILE_ATTRIBUTE_SYSTEM)
            if os.path.isdir(folder_path):
                desktop_ini = os.path.join(folder_path, "desktop.ini")
                if os.path.exists(desktop_ini):
                    os.remove(folder_path+"\desktop.ini")
                    with open(desktop_ini, "w") as ini_file:
                        ini_file.write("[.ShellClassInfo]\n")
                        ini_file.write("IconFile={}\icon.ico\n".format(self.location))
                        ini_file.write("IconIndex=0")
                else:
                    with open(desktop_ini, "w") as ini_file:
                        ini_file.write("[.ShellClassInfo]\n")
                        ini_file.write("IconFile={}\icon.ico\n".format(self.location))
                        ini_file.write("IconIndex=0")

                # Применение изменений
                shell.SHChangeNotify(
                    shellcon.SHCNE_ASSOCCHANGED, shellcon.SHCNF_IDLIST, None, None)
                