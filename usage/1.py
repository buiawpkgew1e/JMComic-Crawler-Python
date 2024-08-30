list2 = [
    '1','2','3','4','5','6','7'
    ]

# 下方填入你要下载的本子的id，一行一个，每行的首尾可以有空白字符
jm_albums = '''
1
2
3
4
334761
5
6
7
8
'''
# 去除空白字符并转换为集合去重，然后转换回列表
jm_albums_set = {x.strip() for x in jm_albums.splitlines() if x.strip()}
print(f"共jm_albums_set: {jm_albums_set}")
print("##################")
# 找到不在 list2 中的唯一ID
unique_ids = [x for x in jm_albums_set if x not in list2]
print(f"以下ID在 list2 中不存在：\n{unique_ids}")
print("##################")
# 将去重后的结果保存到文件
with open('list2.txt', 'w') as file:
    for item in unique_ids:
        file.write(f"{item}\n")
print(f"结果已保存到 list2.txt 文件中。")
import os

A = ['0']
# 读取文件 list2.txt 中的数字
file_path = 'list2.txt'
try:
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                number = line.strip()
                if number and number not in A:
                    A.append(number)
    else:
        print(f"文件 {file_path} 不存在。")
except Exception as e:
    print(f"读取文件时发生错误: {e}")

# 将结果保存到文件
output_file_path = 'final_list.txt'
try:
    with open(output_file_path, 'w') as file:
        for item in A:
            file.write(f"{item}\n")
    print(f"结果已保存到 {output_file_path} 文件中。")
except Exception as e:
    print(f"保存文件时发生错误: {e}")
