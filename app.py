import tkinter as tk
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import re


def crawl_a_page(url):
    page_data = {}

    def find_first_with_pattern(lst, pattern):
        compiled_pattern = re.compile(pattern)
        return next((i for i, item in enumerate(lst) if compiled_pattern.search(item)), 0)

    
    driver = webdriver.Chrome()
    driver.get(url)


    
    product_name = driver.find_element(By.XPATH,'//*[@id="main"]/dl/dd[1]/div[2]/ul/li[1]/h3').text
    page_data['product_name']=product_name

    
    product_category = driver.find_element(By.XPATH,'//*[@id="main"]/dl/dd[1]/div[2]/ul/li[2]').text
    page_data['product_category']=product_category.split('：')[1]

    
    english_name = driver.find_element(By.XPATH,'//*[@id="main"]/dl/dd[1]/div[2]/ul/li[3]/h3').text
    # page_data['english_name']=english_name

    
    license_number = driver.find_element(By.XPATH,'//*[@id="main"]/dl/dd[1]/div[2]/ul/li[4]/h3').text
    page_data['license_number']=license_number

    
    main_specifications = driver.find_element(By.XPATH,'//*[@id="main"]/dl/dd[1]/div[2]/ul/li[5]').text
    page_data['main_specifications']=main_specifications.split('：')[1]

    
    commodity_info = driver.find_element(By.XPATH,'//*[@id="main"]/dl/dd[2]').text
    commodity_info = commodity_info.split('\n')
    # page_data['commodity_info']=commodity_info

    
    # index = find_first_with_pattern(commodity_info,'商品名称')
    # commodity_name = commodity_info[index]
    # commodity_name = commodity_name.split('：')[1]
    # page_data['commodity_name']=commodity_name


    
    index = find_first_with_pattern(commodity_info,'·包\u3000\u3000装')
    commodity_pack = commodity_info[index].split('：')[1]
    page_data['commodity_pack']=commodity_pack

    
    index1 = find_first_with_pattern(commodity_info,'用\u3000\u3000途：')
    index2 = find_first_with_pattern(commodity_info,'科室类别：')
    if index1+1 != index2:
        commodity_use = []
        for index in range(index1+1,index2):
            commodity_use.append(commodity_info[index])
        commodity_use = "".join(commodity_use)
    else:
        commodity_use = commodity_info[index1].split("：")[1]
    page_data['commodity_use']=commodity_use

    
    index = find_first_with_pattern(commodity_info,'科室类别')
    commodity_department = commodity_info[index].split('：')[1]
    page_data['commodity_department']=commodity_department

    
    index1 = find_first_with_pattern(commodity_info,'产品说明')
    if index1 != 0:
        commodity_instrutions = []
        for index in range(index1+1,len(commodity_info)):
            commodity_instrutions.append(commodity_info[index])
        commodity_instrutions = "".join(commodity_instrutions)
    else:
        commodity_instrutions = None
    page_data['commodity_instrutions']=commodity_instrutions

    
    company = driver.find_element(By.XPATH,'//*[@id="main"]/dl/dd[3]/ul/li[2]/h3/a').text
    page_data['company']=company

    
    contact = driver.find_element(By.XPATH,'//*[@id="main"]/dl/dd[3]/ul/li[3]').text
    contact = contact.split('：')[1]
    page_data['contact']=contact

    driver.quit()

    return page_data


def get_all_beauty_links():
    driver = webdriver.Chrome()
    links = []
    for i in range(1,7):
        driver.get(f'http://www.chinamedevice.cn/product/12/11/1128/{i}.html')
        items = driver.find_elements(By.CSS_SELECTOR, 'a.green.fb.f13')
        for item in items:
            links.append(item.get_attribute('href'))
    
    return list(set(links))

def get_rehabilitation_nursing_links():
    driver = webdriver.Chrome()
    links = []
    for i in range(1,29):
        driver.get(f'https://www.chinamedevice.cn/product/12/11/1130/{i}.html')
        items = driver.find_elements(By.CSS_SELECTOR, 'a.green.fb.f13')
        for item in items:
            links.append(item.get_attribute('href'))
    
    return list(set(links))

def get_links(url):
    driver = webdriver.Chrome()
    links = []
    driver.get(url)
    items = driver.find_elements(By.CSS_SELECTOR, 'a.green.fb.f13')
    for item in items:
        links.append(item.get_attribute('href'))
    driver.quit()
    return list(set(links))


def display_input():
    # 获取用户输入的字符串
    user_input = entry.get()
    
    data_list = []
    links = get_links(user_input)
    for url in links:
        data = crawl_a_page(url)
        data_list.append(data)
    df = pd.DataFrame(data_list)
    df.to_csv('/Users/wxk/Desktop/data.csv')

    root.destroy()

# 创建主窗口
root = tk.Tk()
root.title("使用 Entry 接收字符串示例")

# 创建标签提示用户输入
label = tk.Label(root, text="请输入要爬取的网站:")
label.pack(pady=5)

# 创建 Entry 控件
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# 创建按钮，当点击时调用 display_input 函数
submit_button = tk.Button(root, text="提交", command=display_input)
submit_button.pack(pady=10)


# 启动事件循环
root.mainloop()
