import difflib

# 手动输入text1到text5
text1 = input("请输入第一个文本路径：")
text2 = input("请输入第二个文本路径：")
text3 = input("请输入第三个文本路径：")
text4 = input("请输入第四个文本路径：")
text5 = input("请输入第五个文本路径：")

# 创建 SequenceMatcher 对象
differ1 = difflib.SequenceMatcher(None, text1, text2)
differ2 = difflib.SequenceMatcher(None, text2, text3)
differ3 = difflib.SequenceMatcher(None, text3, text4)
differ4 = difflib.SequenceMatcher(None, text4, text5)

differ_list = [differ1, differ2, differ3, differ4]

# 获取差异的部分
for differ in differ_list:
    differences = differ.get_opcodes()

    for tag, i1, i2, j1, j2, a1, a2, b1, b2, c1, c2 in differences:
        if tag == 'replace':
            print(f"Replace {text1[i1:i2]} with {text2[j1:j2]}")
            # 将文本路径的字符转换为数字
            num1 = int(''.join(filter(str.isdigit, text1[i1:i2])))
            num2 = int(''.join(filter(str.isdigit, text2[j1:j2])))
            num3 = int(''.join(filter(str.isdigit, text2[a1:a2])))
            num4 = int(''.join(filter(str.isdigit, text2[b1:b2])))
            num5 = int(''.join(filter(str.isdigit, text2[c1:c2])))
            
            # 判断num的大小
            if num1 > num2:
                diff1 = num1 - num2
            else:
                diff1 = num2 - num1
            if num2 > num3:
                diff2 = num2 - num3
            else:
                diff2 = num3 - num2
            if num3 > num4:
                diff3 = num3 - num4
            else:
                diff3 = num4 - num3
            if num4 > num5:
                diff4 = num4 - num5
            else:
                diff4 = num5 - num4
            print(f"Numeric Difference: {diff1}")
            print(f"Numeric Difference: {diff2}")
            print(f"Numeric Difference: {diff3}")
            print(f"Numeric Difference: {diff4}")
        elif tag == 'delete':
            print(f"Delete {text1[i1:i2]}")
        elif tag == 'insert':
            print(f"Insert {text2[j1:j2]}")
        elif tag == 'equal':
            print(f"Equal: {text1[i1:i2]}")
