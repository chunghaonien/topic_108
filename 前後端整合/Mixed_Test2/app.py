from package import *
import time

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    web_browser_window = WebBrowserWindow(main_window)
    web_browser_window.scraping_button.clicked.connect(web_browser_window.scrape_data)
    
    app.exec_()