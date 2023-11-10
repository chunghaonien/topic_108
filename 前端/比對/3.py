def compare_and_display(data):
    # Step 1: 將取得的資料切割開來
    data_list = data.split(',')

    # Step 2: 將每筆資料分組，進行比較並儲存相異部分
    differences = []
    for i in range(len(data_list) - 1):
        group1 = data_list[i]
        group2 = data_list[i + 1]

        # 比較兩個組的不同部分，顯示具體差異
        diff = ''.join(f'+{ord(c2) - ord(c1)}' if c1 != c2 else c1 for c1, c2 in zip(group1, group2))
        differences.append(diff)

    # Step 3: 將所有相異的資料進行相減，並顯示出來
    result = '\n'.join(differences)
    print(result)

# 資料範例
data = [
    'html[1]/body[1]/div[1]/div[6]/div[1]',
    'html[1]/body[1]/div[1]/div[6]/div[3]',
    'html[1]/body[1]/div[1]/div[6]/div[3]',
    'html[1]/body[1]/div[1]/div[6]/div[4]',
    'html[1]/body[1]/div[1]/div[6]/div[1]',
]

# 將資料合併成一個字串
data_str = ','.join(data)

# 呼叫函式進行比較和顯示
compare_and_display(data_str)
