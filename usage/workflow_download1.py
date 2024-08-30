import os
import time
from threading import current_thread

from jmcomic import *
from jmcomic.cl import JmcomicUI

# 下方填入你要下载的本子的id，一行一个，每行的首尾可以有空白字符
jm_albums = '''
302433
397749
460809
403910
334761
427669
427679
467745
467506
385043
262289
303004
300389
245445
291220
475841
334745
179337
187884
309334
239483
465549
463812
'''

# 单独下载章节
jm_photos = '''


'''

def str_to_set(text):
    return set(line.strip() for line in text.split('\n') if line.strip())

def get_env_value(name, default, trim_pairs=('[]', '""', "''")):
    value = os.getenv(name, default)
    if value is None or value == '':
        return default

    for pair in trim_pairs:
        if value.startswith(pair[0]) and value.endswith(pair[1]):
            value = value[1:-1]

    return value

def get_id_set(env_name, given_text):
    aid_set = set()
    for text in [given_text, get_env_value(env_name, '')]:
        aid_set.update(str_to_set(text))
    return aid_set

def create_option(file_path):
    # 读取 option 配置文件
    option = JmOption(file_path)

    # 支持工作流覆盖配置文件的配置
    cover_option_config(option)

    return option

def cover_option_config(option):
    dir_rule = get_env_value('DIR_RULE', None)
    if dir_rule:
        option.dir_rule = DirRule(dir_rule, base_dir=option.dir_rule.base_dir)

    impl = get_env_value('CLIENT_IMPL', None)
    if impl:
        option.client.impl = impl

    suffix = get_env_value('IMAGE_SUFFIX', None)
    if suffix:
        option.download.image.suffix = fix_suffix(suffix)

def log_before_raise():
    jm_download_dir = get_env_value('JM_DOWNLOAD_DIR', workspace())
    os.makedirs(jm_download_dir, exist_ok=True)

    def decide_filepath(e):
        resp = e.context.get(ExceptionTool.CONTEXT_KEY_RESP, None)
        suffix = resp.url if resp else str(time.time())
        name = '-'.join(fix_windir_name(part) for part in [e.description, current_thread().name, suffix])
        return f'{jm_download_dir}/【出错了】{name}.log'

    def exception_listener(e):
        path = decide_filepath(e)
        content = [str(type(e)), e.msg]
        content.extend(f'{k}: {v}' for k, v in e.context.items())
        if resp := e.context.get(ExceptionTool.CONTEXT_KEY_RESP):
            content.append(f'响应文本: {resp.text}')
        write_text(path, '\n'.join(content))

    JmModuleConfig.register_exception_listener(JmcomicException, exception_listener)

def main():
    album_id_set = get_id_set('JM_ALBUM_IDS', jm_albums)
    photo_id_set = get_id_set('JM_PHOTO_IDS', jm_photos)

    helper = JmcomicUI()
    helper.album_id_list = list(album_id_set)
    helper.photo_id_list = list(photo_id_set)

    option = create_option(os.path.abspath(os.path.join(__file__, '../../assets/option/option_workflow_download.yml')))
    helper.run(option)
    option.call_all_plugin('after_download')

if __name__ == '__main__':
    main()
