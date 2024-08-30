list2 = [
    '1','2','3','4','5','6'
    ]

# 下方填入你要下载的本子的id，一行一个，每行的首尾可以有空白字符
jm_albums = '''
1
2
3
4
334761
5
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