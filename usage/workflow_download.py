
list2 = [
    '438055','450850','421045','372005','400995','400314','400308','334745','378628','351601','350287','340044','334761','334739','421055','359855','419021','359853','414125','355620','401484','359547','407816','347564','416152','345426','416643','342827','416660','399326','419020','368703','408314','376160','405306','404404','364360','404380','401119','422448','422449','423370','424778','437567','436327','433255','435226','432467',
    '455049','463032','461099','463946','461152','459264','459265','460809','457448','458021','455381','417119','444342','447019','445815','294556','454451','454129','454404'
    ]
list1 = [
    '387074', '444521','453364','430743','453642','453790','387169', '310665', '302556', '302103', '303204', '303148', '71828', '278262', '293825', '294577', '297484', '234454', '300231', '300260', '300734', '300561', '301141', '301672', '391073', '301144', '301693', '301912', '301825', '288653', '288071', '232935', '239296', '237624', '235205', '240139', '242668', '245399', '243835', '248539', '250593', '251944', '252906', '252448', '253855', '255193', '256936', '259942', '262048', '263527', '217588', '218679', '214403', '219409', '223348', '224268', '224280', '224270', '224269', '226002', '229845', '230404', '230286', '230662', '230802', '184462', '131273', '189544', '189313', '189220', '190136', '190046', '192358', '367512', '199285', '205535', '205465', '205614', '204306', '209896', '209823', '150789', '142985', '121283', '149083', '150533', '151479', '152093', '158166', '168048', '180649', '180803', '163562', '181886', '184705', '114764', '116259', '87571', '60502', '102239', '125080', '127730', '136210', '136204', '137450', '138483', '183007', '267502', '140635', '140963', '62115', '65844', '65947', '66278', '67024', '70749', '76847', '78012', '78050', '92255', '92491', '99150', '99349', '101888', '102433', '112948', '111480', '34534', '37682', '39198', '40009', '40832', '42609', '42608', '49385', '54060', '54162', '54507', '54408', '54233', '57968', '16847', '17799', '19305', '21620', '25207', '24009', '26739', '26994', '27881', '32533', '13990', '23530', '32574', '32633', '32893', '33908', '33911', '33548', '271', '816', '2882', '2330', '3766', '4199', '4048', '4243', '5154', '5779', '6315', '8750', '9524', '10712', '16531', '5500', '14414', '2582', '81084', '225017', '119130', '245966', '114143', '380098', '372722', '247120', '217272', '104638', '196679', '113257', '148558', '208841', '333721', '181482', '260291', '225768', '330269', '376628', '225812', '330967', '271953', '13918', '99493', '81213', '8975', '317716', '143216', '10594', '14626', '101359', '226063', '288246', '283283', '249383', '292011', '283240', '241446', '73667', '228195', '103295', '210497', '103294', '148297', '193127', '231913', '245809', '285843', '191563', '227083', '6631', '391685', '379728', '388407', '385477', '217732', '387413', '383975', '379717', '376752', '375747', '376751', '366289', '368626', '357649', '357476', '350275', '392871', '396008', '395704', '395080', '394636', '346545', '2527', '125813', '336789', '340355', '188309', '335007', '198123', '251182', '122349', '290605', '295042', '263925', '195007', '275510', '206450', '181632', '142459', '198154', '216056', '271262', '280300', '304803', '379386', '317071', '340494', '291605', '387661', '387660', '387659', '387655', '314909', '277089', '274115', '309353', '207558', '331249', '224063', '347096', '244810', '401196', '401183', '401302', '401465', '90063', '403293', '404981', '405010', '405273', '407371', '399385', '419619', '325333', '405120', '417146', '422129', '422850', '422816', '422865', '423209', '423408', '423596', '423863', '424511', '425022', '211700', '422127', '417454', '427434', '425452', '426550', '86076', '427675', '427673',
    '431433','432007','438251','444422','444110','439123','440097','439570',
    '465320','463960','473271','473999','475841','477310','477104','440190','439633','439634','442208','449105','448498','446483','454458'
    ]

from jmcomic import *
from jmcomic.cl import get_env, JmcomicUI

# 下方填入你要下载的本子的id，一行一个。
# 每行的首尾可以有空白字符
# 你也可以填入本子网址，程序会识别出本子id
# 例如:
# [https://18comic.vip/album/452859/mana-ディシア-1-原神-中国語-無修正] -> [452859]
#
jm_albums = '''
458021
482298
244810
485313
485133
485009
482556
482554
482762


'''

# 单独下载章节
jm_photos = '''


'''


def get_id_set(env_name):
    aid_set = set()
    for text in [
        jm_albums,
        (get_env(env_name, '')).replace('-', '\n'),
    ]:
        aid_set.update(str_to_set(text))

    return aid_set


def main():
    album_id_set = get_id_set('JM_ALBUM_IDS')
    photo_id_set = get_id_set('JM_PHOTO_IDS')

    helper = JmcomicUI()
    helper.album_id_list = list(album_id_set)
    helper.photo_id_list = list(photo_id_set)

    helper.run(get_option())


def get_option():
    # 读取 option 配置文件
    option = create_option('../assets/config/option_workflow_download.yml')

    # 支持工作流覆盖配置文件的配置
    cover_option_config(option)

    # 覆盖client实现类，实现把请求错误的html下载到文件，方便GitHub Actions下载查看日志
    hook_debug(option)

    # 登录，如果有配置的话
    login_if_configured(option.build_jm_client())

    return option


def cover_option_config(option: JmOption):
    dir_rule = get_env('DIR_RULE', None)
    if dir_rule is not None:
        the_old = option.dir_rule
        the_new = DirRule(dir_rule, base_dir=the_old.base_dir)
        option.dir_rule = the_new


def login_if_configured(client):
    # 检查环境变量中是否有禁漫的用户名和密码，如果有则登录
    # 禁漫的大部分本子，下载是不需要登录的，少部分敏感题材需要登录
    # 如果你希望以登录状态下载本子，你需要自己配置一下GitHub Actions的 `secrets`
    # 配置的方式很简单，网页上点一点就可以了
    # 具体做法请去看官方教程：https://docs.github.com/en/actions/security-guides/encrypted-secrets
    # 萌新注意！！！如果你想 `开源` 你的禁漫帐号，你也可以直接把账号密码写到下面的代码😅
    username = get_env('JM_USERNAME', None)
    password = get_env('JM_PASSWORD', None)
    if username is not None and password is not None:
        client.login(username, password, True)
        print_eye_catching(f'登录禁漫成功')


# noinspection PyUnusedLocal
def hook_debug(option):
    jm_download_dir = get_env('JM_DOWNLOAD_DIR', workspace())
    mkdir_if_not_exists(jm_download_dir)

    class RaiseErrorAwareClient(JmHtmlClient):

        @classmethod
        def raise_request_error(cls, resp, msg=None):
            from common import write_text, fix_windir_name
            write_text(
                f'{jm_download_dir}/{fix_windir_name(resp.url)}',
                resp.text
            )

            return super().raise_request_error(resp, msg)

    JmModuleConfig.CLASS_CLIENT_IMPL['html'] = RaiseErrorAwareClient


if __name__ == '__main__':
    main()
