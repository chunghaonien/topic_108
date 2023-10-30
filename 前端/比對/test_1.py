import difflib

text1 = "html[1]/body[1]/div[2]/div[1]"
text2 = "html[1]/body[1]/div[3]/div[1]"

# 创建 SequenceMatcher 对象
differ = difflib.SequenceMatcher(None, text1, text2)

# 获取差异的部分
differences = differ.get_opcodes()

for tag, i1, i2, j1, j2 in differences:
    if tag == 'replace':
        print(f"Replace {text1[i1:i2]} with {text2[j1:j2]}")
    elif tag == 'delete':
        print(f"Delete {text1[i1:i2]}")
    elif tag == 'insert':
        print(f"Insert {text2[j1:j2]}")
    elif tag == 'equal':
        print(f"Equal: {text1[i1:i2]}")

# 输出差异的相关性
similarity_ratio = differ.ratio()
print(f"Similarity ratio: {similarity_ratio}")
