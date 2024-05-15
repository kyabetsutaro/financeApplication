import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


import time
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs


class Application(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=700, height=500,
                         borderwidth=1, relief='groove')
        self.root = root
        self.pack()
        self.pack_propagate(0) # type: ignore
        self.create_widgets()
        self.frame = tk.Frame(self.root)
        
       
        
    
    
    def create_widgets(self):
        # 閉じるボタン
        quit_btn = tk.Button(self)
        quit_btn['text'] = '閉じる'
        quit_btn['command'] = self.root.destroy # type: ignore
        quit_btn.pack(side=tk.BOTTOM)
        

        # テキストボックス
        self.text_box = tk.Entry(self)
        self.text_box['width'] = 10
        self.text_box.place(x=70, y=10)
        
        
        # 実行ボタン
        submit_btn = tk.Button(self)
        submit_btn['text'] = '実行'
        submit_btn['command'] = self.get_url_info
        submit_btn.place(x=150, y=5)
        
        # ラベル
        label_1 = tk.Label(self, text=u'証券コード : ')
        label_1.place(x=5, y=10)
        
        
        # 結果を出力
        self.message = tk.Message(self)
        self.message['width'] = 500
        self.message.place(x=200, y=10)
        
        self.message2 = tk.Message(self)
        self.message2['width'] = 500
        self.message2.place(x=10, y=50)
        
        self.message3 = tk.Message(self)
        self.message3['width'] = 500
        self.message3.place(x=10, y=75)
        
        # #canvas
        
   
        
        
        
        
        
        
        
        
        
        

        
    # 時価総額などの情報を収集する   
    def get_url_info(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        base_url = "https://finance.yahoo.co.jp"        
        self.driver.get(base_url)
        time.sleep(3)
        symbol = self.text_box.get()
        
        form_elements = self.driver.find_elements(By.TAG_NAME, "form")
        pagenation_element = form_elements[1].find_element(By.TAG_NAME, "input").send_keys(symbol)
        button_elements = self.driver.find_elements(By.TAG_NAME, "button")
        button_elements[2].click()        
            
        # 証券情報を収集する
        time.sleep(7)
        result1 = self.driver.find_elements(By.XPATH, '//h2[@class="_6uDhA-ZV"]')
        if len(result1) == 0:
            self.message['text'] = '該当なし'
            self.message2['text'] = ''
            self.message3['text'] = ''
            self.canvas.draw()
            self.driver.quit()
        else:
            # 企業名
            for i in result1:
                result = i.text
                self.message['text'] = '企業名：' + result
                # 時価総額          
                result2 = self.driver.find_elements(By.XPATH, '//span[@class="_3rXWJKZF _11kV6f2G"]') 
                result3 = self.driver.find_elements(By.XPATH, '//span[@class="_2SD5_rym _3uht-s3d"]')               
                self.message2['text'] = '時価総額：' + str(result2[7].text) + str(result3[2].text)
                # 配当利回り                
                self.message3['text'] = '利回り：' + str(result2[9].text) + '%'
                
                
            # グラフを描画
            self.grahf_info()
                
    
    #　株のグラフを作成
    def grahf_info(self):
        # 時系列を呼び込む
        time_button_elements = self.driver.find_elements(By.CLASS_NAME, "_3sZDYuuc")
        time_button_elements[8].click()

        # 価格の日付と終値を収集
        date = []
        price = []
        time.sleep(15)
        
        
        date_elements = [self.driver.find_elements(By.CSS_SELECTOR, "._2ZqX1qip")]
        for i in range(20):
            date_1 = date_elements[0][i].text.split()
            date.append(date_1[0])
            num_str = date_1[4]
            num_int = int(num_str.replace(',', ''))
            price.append(num_int)

        date_reverse = [i for i in reversed(date)]
        price_reverse = [i for i in reversed(price)]
        self.driver.quit()

        self.fig, self.ax = plt.subplots(figsize=(5, 2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().place(x=100, y=250)
        
        self.ax.plot(date_reverse, price_reverse, label="")
        self.ax.grid()
        self.canvas.draw()
        
        
        
        
        
        
        
        
                
                
        
        
        
        
        
def main():
    
    root = tk.Tk()
    root.title("証券情報")
    root.geometry('800x600')
    root.resizable(False, False)
    app = Application(root=root)
    app.mainloop()
    
if __name__ == '__main__':
    main()


