data = ['xpath', "['[新聞] 百年大病院 陽明交大醫院歡慶128歲,html[1]/body[1]/div[2]/div[2]/div[2]/div[2]/a[1]'", "'什麼意思?,html[1]/body[1]/div[2]/div[2]/div[3]/div[2]/a[1]']"]
dou_data = []
dou_data.append(data)

# 去除不需要的内容
cleaned_data = [item.replace("'xpath'", "").replace('"[', "").replace('"]', "").strip() for item in dou_data[0]]

# 打印结果
for cleaned_item in cleaned_data:
    print(cleaned_item)
