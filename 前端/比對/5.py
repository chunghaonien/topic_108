import re

# 原始文本
text = '反白內容: 離開。若您已滿十八歲，亦不可將本區之內容派發、傳閱、出售、出租、交給或借予年齡未滿18歲的人士瀏覽，或將 , {html[1]/body[1]/div[1]/div[1]/p[3]}'

# 使用正则表达式提取大括号内的内容
result = re.search(r'\{(.+?)\}', text)

# 打印结果
if result:
    extracted_content = result.group()
    print(extracted_content)
else:
    print("未找到大括号内的内容")
