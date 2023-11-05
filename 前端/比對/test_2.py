import difflib

# 手动输入text1和text2
text1 = input("請输入第一个文本路徑：")
text2 = input("請输入第二个文本路徑")
text3 = input("請输入第三个文本路徑")
text4 = input("請输入第四个文本路徑")
text5 = input("請输入第五个文本路徑")

# 创建 SequenceMatcher 对象
differ1 = difflib.SequenceMatcher(None, text1, text2)
differ2 = difflib.SequenceMatcher(None, text2, text3)
differ3 = difflib.SequenceMatcher(None, text3, text4)
differ4 = difflib.SequenceMatcher(None, text4, text5)

# 获取差异的部分
differ_list = [differ1, differ2, differ3, differ4]

for differ in differ_list:
    differences = differ.get_opcodes()

    for tag, i1, i2, j1, j2 in differences:
        if tag == 'replace':
            print(f"Replace {text1[i1:i2]} with {text2[j1:j2]}")
            # 将文本路径的字符转换为数字，然后相减
            num1 = int(''.join(filter(str.isdigit, text1[i1:i2])))
            num2 = int(''.join(filter(str.isdigit, text2[j1:j2])))
            diff = num2 - num1
            print(f"Numeric Difference: {diff}")
        elif tag == 'delete':
            print(f"Delete {text1[i1:i2]}")
        elif tag == 'insert':
            print(f"Insert {text2[j1:j2]}")
        elif tag == 'equal':
            print(f"Equal: {text1[i1:i2]}")