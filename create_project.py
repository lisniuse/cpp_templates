import os
import shutil
import json
import argparse
import sys

class ProjectCreator:
    def __init__(self, config_path='create_config.json'):
        """
        初始化 ProjectCreator 类，加载配置文件并设置成员变量

        :param config_path: 配置文件路径，默认为 'create_config.json'
        """
        self.config_path = config_path
        self.config = self.load_config()
        if self.config and self.validate_config():
            self.project_name = self.config['projectName']
            self.entry_file = self.config['entryFile']
            self.project_type = self.config['type']
            self.vcpkg_dir = self.config['vcpkgDir']
            self.target_dir = self.config['targetDir']
            self.open_dir = self.config.get('openDir', False)
            self.project_path = os.path.join(self.target_dir, self.project_name)

    def load_config(self):
        """
        加载配置文件

        :return: 配置字典，如果配置文件未找到则返回 None
        """
        if not os.path.exists(self.config_path):
            print("配置文件未找到")
            return None
        with open(self.config_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def validate_config(self):
        """
        验证配置文件中的所有必需键是否存在且不为空

        :return: 如果所有必需键都存在且不为空，返回 True，否则返回 False 并打印错误信息
        """
        required_keys = ['projectName', 'entryFile', 'type', 'vcpkgDir', 'targetDir']
        for key in required_keys:
            if key not in self.config or not self.config[key]:
                print(f"配置文件错误: 缺少必需的键 '{key}' 或值为空")
                return False
        return True

    def copy_template(self):
        """
        复制模板文件夹到目标目录

        :return: 如果模板文件夹存在且复制成功，返回 True，否则返回 False
        """
        src_dir = os.path.join(os.getcwd(), "templates", self.project_type)
        if not os.path.exists(src_dir):
            print(f"模板文件夹 '{self.project_type}' 未找到")
            return False
        shutil.copytree(src_dir, self.project_path)
        return True

    def rename_files(self):
        """
        重命名目标文件夹中的文件，将文件名中的 'VcPkgTemplate' 替换为 project_name，
        对于 .cpp 文件使用 entry_file 的文件名
        """
        blacklist = [ "dll", "mfc" ]
        entry_file_name = os.path.splitext(os.path.basename(self.entry_file))[0]
        for root, _, files in os.walk(self.project_path):
            for file in files:
                old_path = os.path.join(root, file)
                new_file_name = file.replace("VcPkgTemplate", self.project_name)
                if file.endswith('.cpp') and self.project_type not in blacklist:
                    new_file_name = entry_file_name + '.cpp'
                new_path = os.path.join(root, new_file_name)
                os.rename(old_path, new_path)

    def _replace_in_file(self, file_path, replacements, encoding = 'utf-8'):
        """
        在文件中替换指定的占位符

        :param file_path: 文件路径
        :param replacements: 替换字典，键为占位符，值为替换内容
        """
        if not os.path.exists(file_path):
            print(f"文件 '{file_path}' 未找到")
            return
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
        for old, new in replacements.items():
            content = content.replace(old, new)
        with open(file_path, 'w', encoding=encoding) as file:
            file.write(content)

    def update_vcxproj_file(self):
        """
        更新 .vcxproj 文件中的占位符
        """
        vcxproj_file = os.path.join(self.project_path, f"{self.project_name}.vcxproj")
        replacements = {
            "{projectName}": self.project_name,
            "{entryFile}": self.entry_file,
            "{vcpkgDir}": self.vcpkg_dir
        }
        self._replace_in_file(vcxproj_file, replacements)

    def update_sln_file(self):
        """
        更新 .sln 文件中的占位符
        """
        sln_file = os.path.join(self.project_path, f"{self.project_name}.sln")
        replacements = {
            "{projectName}": self.project_name
        }
        self._replace_in_file(sln_file, replacements)

    def update_filters_file(self):
        """
        更新 .filters 文件中的占位符
        """
        filters_file = os.path.join(self.project_path, f"{self.project_name}.vcxproj.filters")
        replacements = {
            "{entryFile}": self.entry_file
        }
        self._replace_in_file(filters_file, replacements)

    def get_all_file_paths(self, directory):
        file_paths = []
        blacklist = [ '.ico', '.aps' ]
        for root, directories, files in os.walk(directory):
            for filename in files:
                if not any(filename.endswith(ext) for ext in blacklist):
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)
        return file_paths
    
    def update_project_name(self):
        all_files = self.get_all_file_paths(self.project_path)
        blacklist = [ ".rc", ".rc2" ]
        for file in all_files:
            replacements = {
                "{projectName}": self.project_name
            }
            encoding = "utf-16"
            if not any(file.endswith(ext) for ext in blacklist):
                encoding = "utf-8"
            self._replace_in_file(file, replacements, encoding=encoding)

    def open_project_directory(self):
        """
        打开项目目录
        """
        if os.name == 'nt':  # Windows
            os.startfile(self.project_path)
        elif os.name == 'posix':  # macOS, Linux
            os.system(f'open "{self.project_path}"' if sys.platform == 'darwin' else f'xdg-open "{self.project_path}"')

    def create_project(self):
        """
        创建项目，包括复制模板文件夹、重命名文件和更新项目文件，最后根据配置决定是否打开目标目录
        """
        if not self.config:
            return
        if not self.copy_template():
            return
        
        self.rename_files()
        if self.project_type == "mfc":
            self.update_project_name()
        self.update_vcxproj_file()
        self.update_sln_file()
        self.update_filters_file()
        print(f"项目 {self.project_name} 已成功创建在 {self.project_path}")
        if self.open_dir:
            self.open_project_directory()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='创建 C++ 项目模板')
    parser.add_argument('config_path', nargs='?', default='create_config.json', 
                        help='配置文件路径，可以是相对路径或绝对路径，默认读取当前目录下的 create_config.json')
    args = parser.parse_args()

    creator = ProjectCreator(config_path=args.config_path)
    creator.create_project()
