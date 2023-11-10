import difflib
import re

def compare_structure(s1, s2):
    # 使用正則表達式比較部分結構
    pattern = re.compile(r'(\d+|\[\])')
    parts1 = pattern.findall(s1)
    parts2 = pattern.findall(s2)

    diff_structure = [f"+{i+1}" for i, (part1, part2) in enumerate(zip(parts1, parts2)) if part1 != part2]

    return diff_structure

def get_diff_with_structure(t1, t2):
    differ = difflib.SequenceMatcher(None, t1, t2)
    opcodes = differ.get_opcodes()
    # print (opcodes)

    diff_with_structure = []

    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'replace':
            # 替換的情況，比較相異地方的結構
            diff_structure = compare_structure(t1[i1:i2], t2[j1:j2])
            if diff_structure:
                # 顯示相異地方，規律性使用 diff_structure[0]
                diff_with_structure.append(f"{t1[:i1]}[{diff_structure[0]}]{t1[i2:i2+len(diff_structure[0])]}{t1[i2+len(diff_structure[0]):]}")
        elif tag == 'delete':
            # 刪除的情況，只顯示刪除前
            diff_structure = compare_structure(t1[i1:i2], "")
            if diff_structure:
                # 顯示相異地方，規律性使用 diff_structure[0]
                diff_with_structure.append(f"{t1[:i1]}[{diff_structure[0]}]{t1[i2:i2+len(diff_structure[0])]}/{t1[i2+len(diff_structure[0]):]}")
        elif tag == 'insert':
            # 插入的情況，只顯示插入後
            diff_structure = compare_structure("", t2[j1:j2])
            if diff_structure:
                # 顯示相異地方，規律性使用 diff_structure[0]
                diff_with_structure.append(f"{t2[:j1]}[{diff_structure[0]}]{t2[j2:j2+len(diff_structure[0])]}/{t2[j2+len(diff_structure[0]):]}")
        # elif tag == 'equal':
        #     # 相等的情況，直接顯示
        #     diff_with_structure.append(f"{t1[:i1]}{t1[i2:]}")

    return diff_with_structure

def get_grouped_data(data):
    grouped_data = []
    for i in range(len(data) - 1):
        grouped_data.append([data[i], data[i+1]])

    return grouped_data


# 新增測試資料
sample_data = [
    'html[1]/body[1]/div[1]/div[6]/div[1]',
    'html[1]/body[1]/div[1]/div[6]/div[3]',
    'html[1]/body[1]/div[1]/div[6]/div[3]',
    'html[1]/body[1]/div[1]/div[6]/div[4]',
    'html[1]/body[1]/div[1]/div[6]/div[7]',
    
]

# 將資料分組
# grouped_data = get_grouped_data(sample_data)

# 使用新的程式進行測試
for i in range(len(sample_data) - 1):
    diff_with_structure = get_diff_with_structure(sample_data[i], sample_data[i+1])
    for diff in diff_with_structure:
        print (diff)
