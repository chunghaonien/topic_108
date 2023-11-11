import difflib
import re

def compare_structure(s1, s2):
    # 使用正則表達式比較部分結構
    pattern = re.compile(r'(\d+|\[\])')
    parts1 = pattern.findall(str(s1))
    parts2 = pattern.findall(str(s2))

    diff_structure = [f"+{i+1}" for i, (part1, part2) in enumerate(zip(parts1, parts2)) if part1 != part2]

    if diff_structure:
        # 將差異以+1的形式表示
        diff_structure[0] = f"+{diff_structure[0][1:]}"
        return diff_structure
    else:
        return []

def get_diff_with_structure(t1, t2):
    differ = difflib.SequenceMatcher(None, t1, t2)
    opcodes = differ.get_opcodes()

    diff_with_structure = []

    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'replace':
            # 替換的情況，比較相異地方的結構
            diff_structure = compare_structure(t1[i1:i2], t2[j1:j2])
            if diff_structure:
                # 顯示相異地方，規律性使用 diff_structure[0]
                diff_with_structure.append(f"{t1[:i1]}[{diff_structure[0]}]{t1[i2:i2+len(diff_structure[0])]}/{t1[i2+len(diff_structure[0]):]}")
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
        elif tag == 'equal':
            # 相等的情況，直接顯示
            diff_structure = compare_structure(t1[i1:i2], t2[j1:j2])
            if diff_structure:
                # 顯示相異地方，規律性使用 diff_structure[0]
                diff_with_structure.append(f"{t1[:i1]}[{diff_structure[0]}]{t1[i2:i2+len(diff_structure[0])]}/{t1[i2+len(diff_structure[0]):]}")

    return diff_with_structure

def get_grouped_data(data):
    grouped_data = []
    for i in range(len(data) - 1):
        grouped_data.append([data[i], data[i+1]])

    return grouped_data

def main(data):
    # 將資料分組
    grouped_data = get_grouped_data(data)

    # 使用新的程式進行測試
    for data in grouped_data:
        diff_with_structure = compare_structure(data[0], data[1])
        print(diff_with_structure)



