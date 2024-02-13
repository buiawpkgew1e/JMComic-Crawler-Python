import os
import os.path
import logging
import argparse
from typing import List, Optional

# 先定义一个获取环境变量的函数
def get_env(name, default):
    value = os.getenv(name, None)
    if value is None or value == '':
        return default
    return value

# 定义一个日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 创建控制台输出处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class JmcomicUI:
    # ... 省略其他方法 ...

    def parse_arg(self):
        # ... 省略其他代码 ...

        args = parser.parse_args()
        option = args.option
        if option == "":
            self.option_path = None
        else:
            self.option_path = os.path.abspath(option)

        # ... 省略其他代码 ...

    def parse_raw_id(self):
        def parse(text):
            from .jm_toolkit import JmcomicText
            try:
                return JmcomicText.parse_to_jm_id(text)
            except Exception as e:
                logger.error(f"Error parsing ID: {e.args[0]}")
                exit(1)

        self.raw_id_list = args.id_list
        self.photo_id_list = [parse(id[1:]) if id.startswith('p') else parse(id) for id in self.raw_id_list if id.startswith('p')]
        self.album_id_list = [parse(id) for id in self.raw_id_list if not id.startswith('p')]

    def run(self, option):
        # ... 省略其他代码 ...

        if len(self.album_id_list) == 0:
            download_photo(self.photo_id_list, option)
        elif len(self.photo_id_list) == 0:
            download_album(self.album_id_list, option)
        else:
            # 同时下载album和photo
            launcher = MultiTaskLauncher()

            launcher.create_task(
                target=download_album,
                args=(self.album_id_list, option)
            )
            launcher.create_task(
                target=download_photo,
                args=(self.photo_id_list, option)
            )

            launcher.wait_finish()

if __name__ == "__main__":
    JmcomicUI().main()