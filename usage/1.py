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
jm_albums_list = list(jm_albums_set)
print(f"共jm_albums_set: {jm_albums_set}")
print(f"共jm_albums_list: {jm_albums_list}")
# 将去重后的结果保存到文件
with open('list2.txt', 'w') as file:
    for item in jm_albums_list:
        file.write(f"{item}\n")
print(f"结果已保存到 unique_jm_albums.txt 文件中。")
print("##################")
# 找到不在 list2 中的ID
A = [x for x in jm_albums_list if x not in list2]
print(f"以下ID在 list2 中不存在：\n{A}")
print(f"共 {len(A)} 个ID不在 list2 中。")    
print("##################")
# 将 list2 转换为字符串格式
B = '\n'.join(list2)
print(f"list2 转换为字符串格式：\n{B}")
print("##################")
# 将 A 添加到 B 的结尾
B_with_A = B + '\n' + '\n'.join(A)
print(f"将 A 添加到 B 的结尾：\n{B_with_A}")
print("##################")
# 将结果保存到文件
with open('output.txt', 'w') as file:
    file.write(B_with_A)

print(f"结果已保存到 output.txt 文件中。")