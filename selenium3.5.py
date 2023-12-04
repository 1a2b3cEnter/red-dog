import re
import csv
import time
import random
import requests
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By


# 设置多个请求头反爬
def get_ua():
    user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 '
        'OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 '
        'Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 '
        'TaoBrowser/2.0 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 '
        'LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X '
        'MetaSr 1.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE '
        '2.X MetaSr 1.0) '
    ]
    user_agent = random.choice(user_agents)
    return user_agent


# 设置登录网址
def login():
    # 将浏览器最大化显示
    driver.maximize_window()
    # 指定加载页面
    driver.get(
        "https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F%3Fcu%3Dtrue%26utm_source%3Dwww.baidu.com%26utm_medium%3Dtuiguang%26utm_campaign%3Dt_1003608409_%26utm_term%3D1e92b18a171a44a480951ab18457597e")
    driver.implicitly_wait(30)
    driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div/div/div[2]/div[1]/a').click()


# 点击页面搜索框
def click(id_data):
    # 隐式等待查找元素30秒，false则退出
    driver.implicitly_wait(30)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[2]/div/div[2]/input").send_keys(id_data)
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[2]/div/div[2]/button").click()
    time.sleep(2)
    data = []
    # 滑动页面到指定元素
    for c in range(1, int(input_number + 1)):
        driver.implicitly_wait(30)
        # 捕获页面标签
        element_data = driver.find_element(By.XPATH, f'//*[@id="J_goodsList"]/ul/li[{c}]/div/div[3]/a')
        price_data = driver.find_element(By.XPATH, f'//*[@id="J_goodsList"]/ul/li[{c}]/div/div[2]/strong/i')
        model_data = driver.find_element(By.XPATH, f'//*[@id="J_goodsList"]/ul/li[{c}]/div/div[3]/a/em')
        brand_data = driver.find_element(By.XPATH, f'//*[@id="J_goodsList"]/ul/li[1]/div/div[5]/span/a')
        # 提取标签中的商品ID
        href = element_data.get_attribute('href')
        html = re.compile(r'm/(?P<num>.*?).html')
        iterator = html.findall(href)
        for j in iterator:
            data.append(int(j))
        # 提取价格和商品名字
        price = price_data.text
        model = model_data.text
        brand = brand_data.text
        pdata.append(price)
        mdata.append(model)
        bdata.append(brand)
    print("<----------请稍等,数据爬取模块正在启用---------->")
    return data


#  点击新的页面的搜索框
def click1(id_data):
    driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/input").clear()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/input").send_keys(id_data)
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/button").click()
    time.sleep(2)
    data = []
    for c in range(1, input_number + 1):
        driver.implicitly_wait(30)
        # 捕获页面标签
        element = driver.find_element(By.XPATH, f'//*[@id="J_goodsList"]/ul/li[{c}]/div/div[3]/a')
        price_data = driver.find_element(By.XPATH, f'//*[@id="J_goodsList"]/ul/li[{c}]/div/div[2]/strong/i')
        model_data = driver.find_element(By.XPATH, f'//*[@id="J_goodsList"]/ul/li[{c}]/div/div[3]/a/em')
        brand_data = driver.find_element(By.XPATH, f'//*[@id="J_goodsList"]/ul/li[1]/div/div[5]/span/a')
        # 提取标签中的商品ID和价格
        href = element.get_attribute('href')
        html = re.compile(r'm/(?P<num>.*?).html')
        iterator = html.findall(href)
        for j in iterator:
            data.append(int(j))
        # 提取价格和商品名字
        price = price_data.text
        model = model_data.text
        brand = brand_data.text
        pdata1.append(price)
        mdata1.append(model)
        bdata1.append(brand)
    print("<----------请稍等,数据爬取模块正在启用---------->")
    return data


# 设置爬取字段并写入文件
def index(product, p_data, m_data, b_data):
    f = open(f"D://{cid}.csv", 'w', newline='', encoding='utf-8-sig')
    fieldnames = ['用户id', '品牌', '型号', '店铺', '评论发布时间', '地区', '价格', '评分', '评论']
    csvwriter = csv.DictWriter(f, fieldnames=fieldnames)
    csvwriter.writeheader()
    site = 0
    p_site = 0
    for production in product:
        site += 1
        for page in range(100):
            url = f'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc' \
                  f'&clientVersion=1.0.0&t=1695028466426&loginType=3&uuid=122270672.1694611322104588022183.1694611322' \
                  f'.1695018169.1695026648.3&productId={production}&score=0&sortType=5&page=' \
                  f'{page}&pageSize=10&isShadowSku=0&fold=1&bbtf=&shield= '
            headers = {'User-Agent': get_ua()}
            response = requests.get(url, headers=headers)
            # for循环遍历，一个一个提取列表里面元素
            for g_index in response.json()['comments']:
                c_id = g_index.get('id')
                content = g_index.get('content')
                date = g_index.get('creationTime')
                location = g_index.get('location')
                score = g_index.get('score')
                csvwriter.writerow(
                    {'用户id': c_id, '品牌': cid, '型号': m_data[p_site], '店铺': b_data[p_site], '评论发布时间': date, '地区': location, '价格': p_data[p_site], '评分': score, '评论': content})
            print(f"爬取第{site}条第{page}页成功!")
        p_site += 1
    print(f"{cid}的{input_number}条数据已经爬完,请于D盘根目录查看！！！")


#  设置提取的文字格式
def test(content, what, name):
    print(content, what, name)
    return content.isalpha()


# 设置应用界面
class GUI:
    # 初始化字符串
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('京东数据获取程序')
        self.root.geometry("500x200+500+250")
        self.V = tk.StringVar()
        self.V1 = tk.IntVar()
        self.frame_1 = tk.Frame(self.root)
        self.testCMD = (self.root.register(test), '%P', '%v', '%W')
        self.label = tk.Label(self.root, bg='grey', text='请输入你爬取的信息(如:联想电脑，松下电冰箱，索尼相机(注意多个品牌以and分隔)', height=1, width=70)
        self.text = tk.Entry(self.root, width=70, textvariable=self.V, validate='key', validatecommand=self.testCMD)
        self.label1 = tk.Label(self.root, text='', height=1, width=70)
        self.label2 = tk.Label(self.root, bg='grey', text='请输入你爬取的店铺条数：', height=1, width=20)
        self.text2 = tk.Entry(self.root, width=12, textvariable=self.V1, validate='key', validatecommand=self.testCMD)
        # Tkinter 文本框控件中第一个字符的位置是 1.0，可以用数字 1.0 或字符串"1.0"来表示。
        # "end"表示它将读取直到文本框的结尾的输入。我们也可以在这里使用 tk.END 代替字符串"end"。
        self.button = tk.Button(self.root, height=1, width=12, bg='green', text='确认爬取并退出', command=self.root.destroy)
        self.interface()

    def interface(self):
        """"界面编写位置"""
        """"row控制行数，column控制列数，colucomspan控制多少列，rowspan控制多少行"""
        self.label.grid(row=0, column=0, columnspan=20)
        self.text.grid(row=1, column=0, columnspan=20)
        self.label1.grid(row=2, column=0, columnspan=20)
        self.label2.grid(row=3, column=0, columnspan=1)
        self.text2.grid(row=3, column=1, columnspan=1)
        self.button.grid(row=4, column=1)


if __name__ == '__main__':
    app = GUI()
    app.root.mainloop()
    # 隐藏"Chrome正在受到自动软件的控制"
    options = webdriver.ChromeOptions()
    # 去掉开发者警告
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 忽略证书错误
    options.add_argument('--ignore-certificate-errors')
    # 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 忽略 DevTools listening on ws://127.0.0.1... 提示
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 初始化配置
    driver = webdriver.Chrome(chrome_options=options)
    login()
    # 定义列表接收数据
    pdata = []
    pdata1 = []
    mdata = []
    mdata1 = []
    bdata = []
    bdata1 = []
    n = 0
    # 获取爬取的数据条数
    input_number = int(app.V1.get())
    # 获取爬取的文本数据
    for app.V.get().split('and')[n] in range(len(app.V.get().split('and'))):
        if n == 0:
            cid = app.V.get().split('and')[n]
            index(click(cid), pdata, mdata, bdata)
            n += 1
        else:
            cid = app.V.get().split('and')[n]
            index(click1(cid), pdata1, mdata1, bdata1)
            n += 1
    input()
