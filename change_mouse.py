import os
import ctypes

path = r"HKEY_CURRENT_USER\Control Panel\Cursors"
cur_loc = r"C:\Users\Eva\Desktop\virus\cursor.cur"

os.system(f"""REG ADD "{path}" /v Arrow /t REG_EXPAND_SZ /d "{cur_loc}" /f""")

ctypes.windll.user32.SystemParametersInfoA(0x57)
