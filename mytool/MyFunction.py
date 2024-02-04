"""
由于视频抓取demo代码过多，将一些处理方法写在这个类。demo中直接调用以简化代码
"""
import yaml

from mytool.MyConfig import MyConfig


class MyFunction:
    """
        写入方法
    """

    @staticmethod
    def file_writing(path, content):
        try:
            with open(path, mode='wb') as f:
                f.write(content)
        except Exception as e:
            print(e)
            return False
        return True

    # 读取配置文件并封装给MyConfig对象
    @staticmethod
    def read_file_config():
        config = MyConfig()
        yamlpath = "../other/file_config.yaml"
        with open(yamlpath, "rb") as f:
            config_list = list(yaml.safe_load_all(f))
            for con in config_list:
                config.html_url = con['URL']
                config.input_path = con['input_path']
                config.output_path = con['output_path']
                config.ts_path = con['ts_path']
                config.headers = con['headers']
        return config
