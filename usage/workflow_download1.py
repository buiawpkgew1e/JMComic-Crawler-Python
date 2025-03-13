import os
import time
from threading import current_thread

from jmcomic import *
from jmcomic.cl import JmcomicUI

list2 = ['438055', '450850', '421045', '372005', '400995', '400314', '400308', '334745', '378628', '351601', '350287', '340044', '334761', '334739', '421055', '359855', '419021', '359853', '414125', '355620', '401484', '359547', '407816', '347564', '416152', '345426', '416643', '342827', '416660', '399326', '419020', '368703', '408314', '376160', '405306', '404404', '364360', '404380', '401119', '422448', '422449', '423370', '424778', '437567', '436327', '433255', '435226', '432467', '455049', '463032', '461099', '463946', '461152', '459264', '459265', '460809', '457448', '458021', '455381', '417119', '444342', '447019', '445815', '294556', '454451', '454129', '454404', '536765', '525248', '521337', '511142', '504980', '511141', '389111', '526664', '524863', '501217', '498248', '490868', '476075', '475487', '459612', '474352', '449869', '443163', '368143', '302433', '262289', '303004', '300389', '291220', '179337', '187884', '309334', '239483', '465549', '463812', '397749', '385043', '467506', '427669', '467745', '403910', '427679', '536763', '534452', '534451', '532414', '532412', '531456', '527313', '527371', '528784', '504316', '245445', '475841']
# 下方填入你要下载的本子的id，一行一个，每行的首尾可以有空白字符
jm_albums = '''
1088903
1088864
1087860
'''
# 去除空白字符并转换为集合去重，然后转换回列表
jm_albums_set = {x.strip() for x in jm_albums.splitlines() if x.strip()}
# 找到不在 list2 中的唯一ID
unique_ids = [x for x in jm_albums_set if x not in list2]
# 将去重后的结果保存到文件
with open('list2.txt', 'w') as file:
    for item in unique_ids:
        file.write(f"{item}\n")
print(f"结果已保存到 list2.txt 文件中。")
import os

# 读取文件 list2.txt 中的数字
file_path = 'list2.txt'
try:
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                number = line.strip()
                if number and number not in list2:
                    list2.append(number)
    else:
        print(f"文件 {file_path} 不存在。")
except Exception as e:
    print(f"读取文件时发生错误: {e}")
list2 = list(dict.fromkeys(list2))
list2.sort()
# 将结果保存到文件
output_file_path = 'final_list.txt'
try:
    with open(output_file_path, 'w') as file:
        file.write(str(list2))
    print(f"结果已保存到 {output_file_path} 文件中。")
except Exception as e:
    print(f"保存文件时发生错误: {e}")

def env(name, default, trim=('[]', '""', "''")):
    import os
    value = os.getenv(name, None)
    if value is None or value == '':
        return default

    for pair in trim:
        if value.startswith(pair[0]) and value.endswith(pair[1]):
            value = value[1:-1]

    return value


def get_id_set(env_name, given):
    aid_set = set()
    for text in [
        given,
        (env(env_name, '')).replace('-', '\n'),
    ]:
        if isinstance(text, list):
            text = '\n'.join(text)
        aid_set.update(str_to_set(text))

    return aid_set


def main():
    album_id_set = get_id_set('JM_ALBUM_IDS', unique_ids)

    helper = JmcomicUI()
    helper.album_id_list = list(album_id_set)

    option = get_option()
    helper.run(option)
    option.call_all_plugin('after_download')


def get_option():
    # 读取 option 配置文件
    option = create_option(os.path.abspath(os.path.join(__file__, '../../assets/option/option_workflow_download.yml')))

    # 支持工作流覆盖配置文件的配置
    cover_option_config(option)

    # 把请求错误的html下载到文件，方便GitHub Actions下载查看日志
    log_before_raise()

    return option


def cover_option_config(option: JmOption):
    dir_rule = env('DIR_RULE', None)
    if dir_rule is not None:
        the_old = option.dir_rule
        the_new = DirRule(dir_rule, base_dir=the_old.base_dir)
        option.dir_rule = the_new

    impl = env('CLIENT_IMPL', None)
    if impl is not None:
        option.client.impl = impl

    suffix = env('IMAGE_SUFFIX', None)
    if suffix is not None:
        option.download.image.suffix = fix_suffix(suffix)


def log_before_raise():
    jm_download_dir = env('JM_DOWNLOAD_DIR', workspace())
    mkdir_if_not_exists(jm_download_dir)

    def decide_filepath(e):
        resp = e.context.get(ExceptionTool.CONTEXT_KEY_RESP, None)

        if resp is None:
            suffix = str(time_stamp())
        else:
            suffix = resp.url

        name = '-'.join(
            fix_windir_name(it)
            for it in [
                e.description,
                current_thread().name,
                suffix
            ]
        )

        path = f'{jm_download_dir}/【出错了】{name}.log'
        return path

    def exception_listener(e: JmcomicException):
        """
        异常监听器，实现了在 GitHub Actions 下，把请求错误的信息下载到文件，方便调试和通知使用者
        """
        # 决定要写入的文件路径
        path = decide_filepath(e)

        # 准备内容
        content = [
            str(type(e)),
            e.msg,
        ]
        for k, v in e.context.items():
            content.append(f'{k}: {v}')

        # resp.text
        resp = e.context.get(ExceptionTool.CONTEXT_KEY_RESP, None)
        if resp:
            content.append(f'响应文本: {resp.text}')

        # 写文件
        write_text(path, '\n'.join(content))

    JmModuleConfig.register_exception_listener(JmcomicException, exception_listener)


if __name__ == '__main__':
    main()
