original_data = str(('True', [('qqq', 3)]))

# 使用 eval() 解析字符串为 Python 对象
evaluated_data = eval(original_data)

# 确保解析后的数据符合预期的格式
if isinstance(evaluated_data, tuple) and len(evaluated_data) == 2:
    # 提取原始数据的第一个元素（字符串 'True'）
    result = [str(evaluated_data[0])]

    # 提取原始数据的第二个元素（列表 [('鍾皓年', 2)]）
    sublist = evaluated_data[1]

    # 判断子列表不为空且至少包含一个元素
    if sublist and len(sublist) > 0:
        # 提取子列表的第一个元素（元组 ('鍾皓年', 2)）
        inner_tuple = sublist[0]

        # 将元组中的元素转换为字符串并添加到结果列表中
        result.extend(map(str, inner_tuple))

    print(result)
else:
    print("解析后的数据格式不符合预期。")
