import difflib

# 手动输入text1到text5
text1 = input("请输入第一个文本路径：")
text2 = input("请输入第二个文本路径：")
text3 = input("请输入第三个文本路径：")
text4 = input("请输入第四个文本路径：")
text5 = input("请输入第五个文本路径：")

# 获取差异的部分
def differences(t1, t2):
    differ = difflib.SequenceMatcher(None, t1, t2)
    differences = differ.get_opcodes()

    for tag, i1, i2, j1, j2 in differences:
        if tag == 'replace':
            return (f"Replace {text1[i1:i2]} with {text2[j1:j2]}")

            # 将文本路径的字符转换为数字
            num1 = int(''.join(filter(str.isdigit, text1[i1:i2])))
            num2 = int(''.join(filter(str.isdigit, text2[j1:j2])))
            num3 = int(''.join(filter(str.isdigit, text2[i1:i2])))
            num4 = int(''.join(filter(str.isdigit, text3[j1:j2])))
            num5 = int(''.join(filter(str.isdigit, text3[i1:i2])))
            num6 = int(''.join(filter(str.isdigit, text4[j1:j2])))
            num7 = int(''.join(filter(str.isdigit, text4[i1:i2])))
            num8 = int(''.join(filter(str.isdigit, text5[j1:j2])))
            print(f"Numeric Difference: {abs(num1 - num2)}")  # 使用abs絕對值
            print(f"Numeric Difference: {abs(num2 - num3)}")
            print(f"Numeric Difference: {abs(num3 - num4)}")
            print(f"Numeric Difference: {abs(num4 - num5)}")
        elif tag == 'delete':
            print(f"Delete {text1[i1:i2]}")
        elif tag == 'insert':
            print(f"Insert {text2[j1:j2]}")
        elif tag == 'equal':
            print(f"Equal: {text1[i1:i2]}")
