import os
import win32api
import win32com
import win32con
from win32com.shell import shell, shellcon

# Путь к иконке
icon_path = r"C:\Users\Eva\Desktop\icon.ico"
# Путь к рабочему столу
desktop_folder = shell.SHGetFolderPath(
    0, shellcon.CSIDL_DESKTOPDIRECTORY, 0, 0)

# Обход всех папок на рабочем столе и замена иконок
for folder_name in os.listdir(desktop_folder):
    folder_path = os.path.join(desktop_folder, folder_name)
    win32api.SetFileAttributes(folder_path,win32con.FILE_ATTRIBUTE_SYSTEM)
    if os.path.isdir(folder_path):
        desktop_ini = os.path.join(folder_path, "desktop.ini")
        if not os.path.exists(desktop_ini):
            with open(desktop_ini, "w") as ini_file:
                ini_file.write("[.ShellClassInfo]\n")
                ini_file.write("IconFile={}\n".format(icon_path))
                ini_file.write("IconIndex=0")
        else:
            with open(desktop_ini, "r+") as ini_file:
                ini_file_content = ini_file.read()
                if "IconFile" not in ini_file_content:
                    ini_file.write("\nIconFile={}".format(icon_path))

        # Применение изменений
        shell.SHChangeNotify(
            shellcon.SHCNE_ASSOCCHANGED, shellcon.SHCNF_IDLIST, None, None)