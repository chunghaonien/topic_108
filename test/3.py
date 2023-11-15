import sys
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QLabel, QFileDialog, QSplitter, QDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSlot, QDateTime, QTimer, QUrl
from PyQt6.QtCore import Qt
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from pynput import mouse, keyboard
from datetime import datetime
import threading
import time
from PyQt6 import QtCore
import subprocess
import os
import re


class MyWebEnginePage(QWebEngineView):
    def __init__(self):
        super().__init__()

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # 设置页面加载完成时的回调函数
        self.browser.page().loadFinished.connect(self.loadFinished)

        # 在浏览器中加载一个网页
        self.browser.setUrl(QUrl("https://www.google.com.tw"))

        # 设置主窗口的布局
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        # 创建按钮用于触发获取XPath信息的操作
        self.get_xpath_button = QPushButton("Get XPath Information")
        self.get_xpath_button.clicked.connect(self.show_element_info)
        layout.addWidget(self.get_xpath_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_element_info(self):
        js_code = '''
        function getPathTo(element) {
            var path = [];
            while (element !== null && element.nodeType === 1) {
                var name = element.tagName.toLowerCase();
                var siblings = element.parentNode.childNodes;
                var index = 1;
                for (var i = 0; i < siblings.length; i++) {
                    var sibling = siblings[i];
                    if (sibling === element) {
                        path.unshift(name + '[' + index + ']');
                        break;
                    }
                    if (sibling.nodeType === 1 && sibling.tagName.toLowerCase() === name) {
                        index++;
                    }
                }
                element = element.parentNode;
            }
            return path.join('/');
        }

        var selectedText = window.getSelection().toString();
        var element = window.getSelection().anchorNode.parentElement;
        var path = getPathTo(element);

        // 将结果通过信号发送给 Python 部分
        selectedText + ' , {' + path + '}';
        '''
        self.browser.page().runJavaScript(js_code, self.handle_js_call)

    @pyqtSlot(result=str)
    def handle_js_call(self, result):
        # 处理 JavaScript 代码的返回结果
        print("XPath information:", result)
        # 这里可以继续处理返回的 XPath 结果，比如存储或展示在界面上

    def loadFinished(self, success):
        # 页面加载完成时的回调函数
        if success:
            print("Page loaded successfully.")
        else:
            print("Failed to load page.")

if __name__ == "__main__":
    app = QApplication([])
    window = BrowserWindow()
    window.show()
    app.exec()
