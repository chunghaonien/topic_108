import urllib.request as req
import urllib.error as err
import tkinter as tk

def get_code():
    url = url_input.get()

    try:
        response = req.urlopen(url)
        content = response.read().decode('UTF-8')
        code_output.delete('1.0', tk.END)
        code_output.insert(tk.END, content)
    except err.URLError as e:
        code_output.delete('1.0', tk.END)
        code_output.insert(tk.END, "發生錯誤：" + str(e))

root = tk.Tk()
root.title('取得網頁程式碼')

url_label = tk.Label(root, text='請輸入網址：')
url_label.pack()

url_input = tk.Entry(root)
url_input.pack()

start_button = tk.Button(root, text='開始', command=get_code)
start_button.pack()

code_label = tk.Label(root, text='程式碼：')
code_label.pack()

code_output = tk.Text(root)
code_output.pack()

root.mainloop()
