import subprocess
import os

# 使用相對路徑啟動另一支程式
script_path = os.path.join(os.path.dirname(__file__), "6.py")
process = subprocess.Popen(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 等待子程式完成並獲取輸出
stdout, stderr = process.communicate()

# 輸出子程式的結果
print("stdout:", stdout.decode(errors='ignore'))
print("stderr:", stderr.decode(errors='ignore'))
