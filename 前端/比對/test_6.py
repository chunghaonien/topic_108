import difflib

# 获取差异的部分
def get_differences(t1, t2):
    differ = difflib.SequenceMatcher(None, t1, t2)
    differences = differ.get_opcodes()
    return differences

# 处理差异标签
def process_differences(differences, t1, t2):
    for tag, i1, i2, j1, j2 in differences:
        if tag == 'replace':
            print(f"Replace {t1[i1:i2]} with {t2[j1:j2]}")
            # 将文本路径的字符转换为数字
            num1 = int(''.join(filter(str.isdigit, t1[i1:i2])))
            num2 = int(''.join(filter(str.isdigit, t2[j1:j2])))
            print(f"Numeric Difference: {abs(num1 - num2)}")  # 使用abs绝对值



if __name__ == "__main__":
    # 手动输入text1到text5
    text1 = input("请输入第一个文本路径：")
    text2 = input("请输入第二个文本路径：")
    text3 = input("请输入第三个文本路径：")
    text4 = input("请输入第四个文本路径：")
    text5 = input("请输入第五个文本路径：")

    # 调用differences函数来比较文本
    diff_1_2 = get_differences(text1, text2)
    process_differences(diff_1_2, text1, text2)

    diff_2_3 = get_differences(text2, text3)
    process_differences(diff_2_3, text2, text3)

    diff_3_4 = get_differences(text3, text4)
    process_differences(diff_3_4, text3, text4)

    diff_4_5 = get_differences(text4, text5)
    process_differences(diff_4_5, text4, text5)

