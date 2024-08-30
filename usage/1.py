list2 = [
    '438055','450850','421045','372005','400995','400314','400308','334745','378628','351601','350287','340044','334761','334739','421055','359855','419021','359853','414125','355620','401484','359547','407816','347564','416152','345426','416643','342827','416660','399326','419020','368703','408314','376160','405306','404404','364360','404380','401119','422448','422449','423370','424778','437567','436327','433255','435226','432467',
    '455049','463032','461099','463946','461152','459264','459265','460809','457448','458021','455381','417119','444342','447019','445815','294556','454451','454129','454404',
    '536765',525248,521337,511142,504980,511141,389111,526664,524863,501217,498248,490868,476075,475487,459612,474352,449869,443163,368143,302433,262289,303004,300389,291220,179337,187884,309334,239483,465549,463812,
    397749,385043,467506,427669,467745,403910,427679,
    536763,534452,534451,532414,532412,531456,527313,527371,528784,504316
    ]
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

# 将结果保存到文件
output_file_path = 'final_list.txt'
try:
    with open(output_file_path, 'w') as file:
        file.write(str(list2))
    print(f"结果已保存到 {output_file_path} 文件中。")
except Exception as e:
    print(f"保存文件时发生错误: {e}")
