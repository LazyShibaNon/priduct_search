import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import time
import csv
import sqlite3

def _pcHome():
    

    wiN1=tk.Toplevel(wiN)
    wiN1.title("pchome24HR")
    wiN1.geometry("800x500")
    
    btN1 = tk.Button(wiN1, text="關閉視窗",bg="Plum", font=("微軟正黑體", 13), width=12, height=1, command=wiN1.destroy)
    btN1.pack() 
    
    sBar=tk.Scrollbar(wiN1)
    sBar.pack(side=tk.RIGHT,fill=tk.Y)
    
    listBox=tk.Listbox(wiN1,width=400,height=200,bg="LemonChiffon", font=("微軟正黑體", 12,"bold"),yscrollcommand=sBar.set)
    listBox.pack(side=tk.BOTTOM,fill=tk.BOTH)
    sBar.config(command=listBox.yview)

    searcH=enteR.get()
    hoW=enteR2.get()
    
    dB=sqlite3.connect(searcH+"-pchome"+".db")
    dB.execute("CREATE TABLE goods (id INTEGER PRIMARY KEY AUTOINCREMENT, product TEXT,	price INTEGER, link TEXT)")
    dB.commit()

    headLess=webdriver.ChromeOptions()
    headLess.add_argument("headless")
    wwW=webdriver.Chrome(options=headLess)

    urL="https://24h.pchome.com.tw/index/v4.1"
    wwW.implicitly_wait(10)
    wwW.get(urL)
    #wwW.maximize_window()
    
    keyWord=wwW.find_element_by_id("keyword")
    
    keyWord.send_keys(searcH)
    keyWord.send_keys(Keys.ENTER)
    
    fileName=searcH+"pchome.csv"

    csvFile=open(fileName,"w",newline="",encoding="utf-8-sig")
    writeR=csv.writer(csvFile)
    writeR.writerow(["標題","價格","超連結"])
    
    counT=1
    runTimes=int(hoW)//20+5
    for vI in range(runTimes):
        wwW.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.3)
        
    souP=wwW.find_element_by_id("ItemContainer")   
    for mySoup in souP.find_elements_by_class_name("col3f"):

        listFile=[]
        
        productName = mySoup.find_element_by_class_name("prod_name").text
        productUrl = mySoup.find_element_by_tag_name("a").get_attribute("href")
        productPrice = mySoup.find_element_by_class_name("value").text
        
        listBox.insert(tk.END,str(counT)+"--"+productName)
        listFile.append(productName)
        listBox.insert(tk.END,"$"+productPrice)
        listFile.append(productPrice)
        listBox.insert(tk.END,productUrl)
        listFile.append(productUrl)
        listBox.insert(tk.END,"------"*25)
        
        
        dB.execute("INSERT INTO goods (product, price, link) 	VALUES (?,?,?)",listFile)
        dB.commit()
        
        writeR.writerow([productName,productPrice,productUrl])

        if counT>=int(hoW):
            break
        counT=counT+1
    dB.close()
    csvFile.close()
    wwW.quit()
    


def _moMo():
    wiN1=tk.Toplevel(wiN)
    wiN1.title("momo購物網")
    wiN1.geometry("800x500")
    
    sBar=tk.Scrollbar(wiN1)
    sBar.pack(side=tk.RIGHT,fill=tk.Y)
    
    btN1 = tk.Button(wiN1, text="關閉視窗",bg="Plum", font=("微軟正黑體", 13), width=12, height=1, command=wiN1.destroy)
    btN1.pack() 

    listBox=tk.Listbox(wiN1,width=400,height=200,bg="LemonChiffon", font=("微軟正黑體", 12,"bold"),yscrollcommand=sBar.set)
    listBox.pack(side=tk.LEFT,fill=tk.BOTH)
    sBar.config(command=listBox.yview)
    
    searcH=enteR.get()
    hoW=enteR2.get()
    
    dB=sqlite3.connect(searcH+"-momo.db")
    dB.execute("CREATE TABLE goods (id INTEGER PRIMARY KEY AUTOINCREMENT, product TEXT,	price INTEGER, link TEXT)")
    dB.commit()
    
    user_agent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    opS=webdriver.ChromeOptions()
    opS.add_argument("--user-agent=%s" % user_agent)
    opS.add_argument("headless")
    wwW=webdriver.Chrome(options=opS)
    
    urL="https://www.momoshop.com.tw"
    
    wwW.implicitly_wait(10)
    #wwW.maximize_window()
    wwW.get(urL)
    keyWord=wwW.find_element_by_name("keyword")
    
    keyWord.send_keys(searcH)
    keyWord.send_keys(Keys.ENTER)

    fileName=searcH+"momo.csv"

    csvFile=open(fileName,"w",newline="",encoding="utf-8-sig")
    writeR=csv.writer(csvFile)
    writeR.writerow(["標題","價格","超連結"])

    counT=1
    runPage=1

    while counT < int(hoW):    
        souP=wwW.find_elements_by_class_name("goodsUrl")
        for mySoup in souP:
            
            listFile=[]
            
            productName = mySoup.find_element_by_class_name("prdName").text
            productPrice = mySoup.find_element_by_class_name("price").text
            productUrl = mySoup.get_attribute("href")
            
            listBox.insert(tk.END,str(counT)+"--"+productName)
            listFile.append(productName)
            listBox.insert(tk.END,productPrice)
            listFile.append(productPrice)
            listBox.insert(tk.END,productUrl)
            listFile.append(productUrl)
            listBox.insert(tk.END,"------"*25)
            
            dB.execute("INSERT INTO goods (product, price, link) 	VALUES (?,?,?)",listFile)
            dB.commit()
            
            writeR.writerow([productName,productPrice,productUrl])
            if counT >= int(hoW):
                break
            counT=counT+1
        runPage=runPage+1
        urL="https://www.momoshop.com.tw/search/searchShop.jsp?keyword="+searcH+"&searchType=1&curPage="+str(runPage)+"&_isFuzzy=0&showType=chessboardType"
        wwW.get(urL)
    dB.close()
    csvFile.close()
    wwW.quit()   
        

def _yahooBuy():
    wiN1=tk.Toplevel(wiN)
    wiN1.title("yahoo購物中心")
    wiN1.geometry("800x500")
    
    sBar=tk.Scrollbar(wiN1)
    sBar.pack(side=tk.RIGHT,fill=tk.Y)
    
    btN1 = tk.Button(wiN1, text="關閉視窗",bg="Plum", font=("微軟正黑體", 13), width=12, height=1, command=wiN1.destroy)
    btN1.pack() 

    listBox=tk.Listbox(wiN1,width=400,height=200,bg="LemonChiffon", font=("微軟正黑體", 12,"bold"),yscrollcommand=sBar.set)
    listBox.pack(side=tk.LEFT,fill=tk.BOTH)
    sBar.config(command=listBox.yview)
    
    searcH=enteR.get()
    hoW=enteR2.get()
    
    dB=sqlite3.connect(searcH+"yahoobuy.db")
    dB.execute("CREATE TABLE goods (id INTEGER PRIMARY KEY AUTOINCREMENT, product TEXT,	price INTEGER, link TEXT)")
    dB.commit()

    myHeader={"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"}

    fileName=searcH+"yahoobuy.csv"

    csvFile=open(fileName,"w",newline="",encoding="utf-8-sig")
    writeR=csv.writer(csvFile)
    writeR.writerow(["標題","價格","超連結"])

    runPage=1
    counT=1
    checK=True
    while checK:
    
        urL="https://tw.buy.yahoo.com/search/product?disp=list&p="+searcH+"&pg="+str(runPage)
        rQ=requests.get(urL,headers=myHeader).text
        souP=BeautifulSoup(rQ,"html5lib")
        soupS=souP.find("ul","listViewList")
        
        for mySoup in soupS.find_all("li","ListItem_listitem_Ik9jn"):
            listFile=[]
                    
            productName = mySoup.find("div","ListItem_detail_EEPbr").a.text.strip()
            productPrice = mySoup.find("div","ListItem_price_2CMKZ").span.text.strip()
            productUrl = mySoup.find("div","ListItem_detail_EEPbr").a["href"]

            listBox.insert(tk.END,str(counT)+"--"+productName)
            listFile.append(productName)
            listBox.insert(tk.END,productPrice)
            listFile.append(productPrice)
            listBox.insert(tk.END,productUrl)
            listFile.append(productUrl)
            listBox.insert(tk.END,"------"*25)
            
            dB.execute("INSERT INTO goods (product, price, link) 	VALUES (?,?,?)",listFile)
            dB.commit()
                
            writeR.writerow([productName,productPrice,productUrl])
            
            if counT >= int(hoW):
                checK=False
                break
            counT=counT+1
        runPage=runPage+1
    
    
    dB.close()
    csvFile.close()

    



def _fridayShopping():

    wiN1=tk.Toplevel(wiN)
    wiN1.title("friday購物網")
    wiN1.geometry("800x500")
    
    sBar=tk.Scrollbar(wiN1)
    sBar.pack(side=tk.RIGHT,fill=tk.Y)
    
    btN1 = tk.Button(wiN1, text="關閉視窗",bg="Plum", font=("微軟正黑體", 13), width=12, height=1, command=wiN1.destroy)
    btN1.pack() 

    listBox=tk.Listbox(wiN1,width=400,height=200,bg="LemonChiffon", font=("微軟正黑體", 12,"bold"),yscrollcommand=sBar.set)
    listBox.pack(side=tk.LEFT,fill=tk.BOTH)
    sBar.config(command=listBox.yview)
    
    searcH=enteR.get()
    hoW=enteR2.get()
    
    dB=sqlite3.connect(searcH+"fridaybuy.db")
    dB.execute("CREATE TABLE goods (id INTEGER PRIMARY KEY AUTOINCREMENT, product TEXT,	price INTEGER, link TEXT)")
    dB.commit()

    user_agent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    opS=webdriver.ChromeOptions()
    opS.add_argument("--user-agent=%s" % user_agent)
    opS.add_argument("headless")
    wwW=webdriver.Chrome(options=opS)
    
    urL="https://shopping.friday.tw/index.html"
    
    wwW.implicitly_wait(10)
    #wwW.maximize_window()
    wwW.get(urL)
    
    keyWord=wwW.find_element_by_id("keyword")
    keyWord.send_keys(searcH)
    keyWord.send_keys(Keys.ENTER)

    fileName=searcH+"fridaybuy.csv"

    csvFile=open(fileName,"w",newline="",encoding="utf-8-sig")
    writeR=csv.writer(csvFile)
    writeR.writerow(["標題","價格","超連結"])

    counT=1
    runPage=1

    while counT < int(hoW):    
        souP=wwW.find_element_by_class_name("product_items_box")
            
        for mySoup in souP.find_elements_by_class_name("search_items"):
            try:
                
                listFile=[]
                
                productName = mySoup.find_element_by_class_name("prod_name").text
                productPrice = mySoup.find_element_by_class_name("price").text
                productUrl = mySoup.find_element_by_tag_name("a").get_attribute("href")

                listBox.insert(tk.END,str(counT)+"--"+productName)
                listFile.append(productName)
                listBox.insert(tk.END,"$ "+productPrice)
                listFile.append(productPrice)
                listBox.insert(tk.END,productUrl)
                listFile.append(productUrl)
                listBox.insert(tk.END,"------"*25)
                
                dB.execute("INSERT INTO goods (product, price, link) 	VALUES (?,?,?)",listFile)
                dB.commit()
                
                writeR.writerow([productName,productPrice,productUrl])
                if counT >= int(hoW):
                    break
                counT=counT+1
            except:
                continue
        runPage=runPage+1
        urL="https://shopping.friday.tw/ec2/search?keyword="+searcH+"&page="+str(runPage)
        wwW.get(urL)
   
    csvFile.close()
    dB.close()
    wwW.quit()


def _exIt():
    qQ=tk.messagebox.askokcancel("提示","確定要結束程式嗎???")
    if qQ:
        wiN.destroy()
    


wiN = tk.Tk()
wiN.title("~購物網查詢~")
wiN.geometry("300x250")
wiN.configure(bg="Bisque")

lbL = tk.Label(wiN,text="請輸入想查詢的商品: ",bg="PowderBlue",  font=("微軟正黑體", 12))
lbL.pack()
enteR=tk.Entry(wiN,font=("微軟正黑體",12),bd=5)
enteR.pack()

lbL2 = tk.Label(wiN,text="輸入想查詢幾筆資料: ",bg="PowderBlue", font=("微軟正黑體", 12))
lbL2.pack()
enteR2=tk.Entry(wiN,font=("微軟正黑體",12),bd=5)
enteR2.pack()

btN1 = tk.Button(wiN, text="pchome24HR",bg="LightBlue", font=("微軟正黑體", 12), width=12, height=1, command=_pcHome)
btN1.place(x=15,y=115) 

btN2 = tk.Button(wiN, text="momo購物網",bg="Khaki", font=("微軟正黑體", 12), width=12, height=1, command=_moMo)
btN2.place(x=150,y=115) 

btN3 = tk.Button(wiN, text="yahoo購物中心",bg="PaleGreen", font=("微軟正黑體", 12), width=12, height=1, command=_yahooBuy)
btN3.place(x=15,y=160)
 
btN4 = tk.Button(wiN, text="friday購物中心",bg="LightPink", font=("微軟正黑體", 12), width=12, height=1, command=_fridayShopping)
btN4.place(x=150,y=160)

btN5 = tk.Button(wiN, text="離開",bg="Thistle", font=("微軟正黑體", 12), width=12, height=1, command=_exIt)
btN5.place(x=85,y=200)

wiN.mainloop()

