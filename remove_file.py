import os
import shutil

class DeleteFile:
    def init(self) -> None:
        self.directory_path = "C:\\"+"\\".join(os.path.dirname(os.path.realpath("__file__")).replace("C:", "").split("\\")[1:3])

    def delete_files_in_folder(self,folder_path):
        files = os.listdir(folder_path)
        
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            
            if os.path.isfile(file_path):
                # Удаляем файл
                os.remove(file_path)
                print(f"Удален файл: {file_path}")

    def delete_files_in_directory(self):
        for root, dirs, files in os.walk(self.directory_path):
            for dir_name in dirs:
                folder_path = os.path.join(root, dir_name)
                self.delete_files_in_folder(folder_path)
                shutil.rmtree(self.directory_path + "\\" + dir_name)
