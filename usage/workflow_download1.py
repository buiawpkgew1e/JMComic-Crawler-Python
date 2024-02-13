import os
import time
import logging
from jmcomic import JmcomicUI, create_option, DirRule, JmOption, JmcomicException
from jmcomic.cl import ExceptionTool

# 更具描述性的变量名，假设list1为专辑ID列表，list2为单个图片ID列表
jm_albums = '''
302433
'''

image_ids = [
    # ... (原来的list2内容)
]

# 日志配置
logging.basicConfig(filename='download.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def load_ids_from_env(env_name, default_value):
    """
    从环境变量加载ID集合，并去除空白字符和指定的首尾字符
    """
    env_value = os.getenv(env_name, default_value).strip()
    trimmed_value = env_value.strip('[]').strip('"\'')
    return set(trimmed_value.split('\n'))

def main():
    # 加载要下载的专辑ID集合
    album_id_set = load_ids_from_env('JM_ALBUM_IDS', jm_albums)
    
    # 加载要下载的图片ID集合
    image_id_set = load_ids_from_env('JM_PHOTO_IDS', '\n'.join(str(id) for id in image_ids))

    # 创建JmcomicUI实例并设置待下载ID列表
    helper = JmcomicUI()
    helper.album_id_list = list(album_id_set.intersection(set(album_ids)))
    helper.photo_id_list = list(image_id_set.intersection(set(image_ids)))

    # 获取选项配置
    option = get_option()

    try:
        helper.run(option)
        option.call_all_plugin('after_download')
    except JmcomicException as e:
        # 异常处理：将错误信息记录到日志中
        logging.error(f'Error occurred while downloading: {str(e)}')
        # 可在此处添加更详细的错误处理逻辑，如保存异常响应文本等

def get_option():
    # 创建并读取option配置文件
    option = create_option(os.path.join(os.path.dirname(__file__), '../../assets/option/option_workflow_download.yml'))

    # 覆盖配置文件中的配置项
    cover_option_config(option)

    # 添加请求错误时的日志记录功能
    log_before_raise()

    return option

def cover_option_config(option: JmOption):
    # 从环境变量获取并覆盖dir_rule与client.impl配置
    dir_rule_env = os.getenv('DIR_RULE')
    if dir_rule_env is not None:
        old_dir_rule = option.dir_rule
        new_dir_rule = DirRule(dir_rule_env, base_dir=old_dir_rule.base_dir)
        option.dir_rule = new_dir_rule

    client_impl = os.getenv('CLIENT_IMPL')
    if client_impl is not None:
        option.client.impl = client_impl

    # 获取并覆盖图片后缀
    suffix = os.getenv('IMAGE_SUFFIX')
    if suffix is not None:
        option.download.image.suffix = fix_suffix(suffix)

def log_before_raise():
    jm_download_dir = os.getenv('JM_DOWNLOAD_DIR', workspace())
    mkdir_if_not_exists(jm_download_dir)

    def exception_listener(e: JmcomicException):
        """
        异常监听器，当发生JmcomicException时，将错误信息写入日志文件
        """
        error_log_content = [type(e), e.msg]
        error_log_content.extend((f'{k}: {v}' for k, v in e.context.items()))
        
        resp = e.context.get(ExceptionTool.CONTEXT_KEY_RESP)
        if resp:
            error_log_content.append(f'Response Text: {resp.text}')

        log_path = f'{jm_download_dir}/【出错了】{time.strftime("%Y%m%d%H%M%S", time.localtime())}.log'
        with open(log_path, 'w') as log_file:
            log_file.write('\n'.join(error_log_content))

    JmModuleConfig.register_exception_listener(JmcomicException, exception_listener)

if __name__ == '__main__':
    main()