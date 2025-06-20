import re
import csv
import time
import random
import requests
import threading
import tkinter as tk
from tkinter import scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class JDCrawler:
    def __init__(self):
        self.driver = self.setup_driver()
        self.headers = {
            'User-Agent': self.get_ua(),
            'Referer': 'https://item.jd.com/'
        }
        self.product_data = []
        self.comments_data = []
        self.running = True
        self.lock = threading.Lock()

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)  # 添加隐式等待
        return driver

    def get_ua(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        ]
        return random.choice(user_agents)

    def login(self):
        try:
            self.driver.maximize_window()
            self.driver.get("https://passport.jd.com/new/login.aspx")

            # 切换到账户登录
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div[1]/div/div/div[2]/div[1]/a'))
            ).click()

            # 等待用户手动登录
            WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="user"]/div[1]/div/a'))
            )

            # 登录后尝试关闭可能的弹窗
            self.close_popups()
            return True
        except TimeoutException:
            return False

    def close_popups(self):
        """关闭各种可能出现的弹窗"""
        try:
            # 尝试关闭可能的弹窗
            close_selectors = [
                '.popup-close',
                '.layer-close',
                '.notice-close',
                '.umc-equity .close',
                '.close-notice'
            ]

            for selector in close_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            element.click()
                            time.sleep(0.5)
                except:
                    pass

            # 尝试关闭优惠券弹窗
            try:
                coupon_close = self.driver.find_element(By.CSS_SELECTOR, '.coupon-close')
                if coupon_close.is_displayed():
                    coupon_close.click()
                    time.sleep(0.5)
            except:
                pass
        except:
            pass

    def search_products(self, keyword, max_items):
        try:
            # 确保在首页
            self.driver.get("https://www.jd.com")
            time.sleep(1)

            # 关闭首页可能的弹窗
            self.close_popups()

            # 搜索框
            search_box = WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="key"]'))

            )

            search_box.clear()
            search_box.send_keys(keyword)

            # 搜索按钮 - 使用CSS选择器提高稳定性
            search_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#search button.button'))
            )

            # 使用JavaScript点击，避免元素被遮挡
            self.driver.execute_script("arguments[0].click();", search_btn)

            # 等待结果加载
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="J_goodsList"]/ul/li[1]'))
            )

            # 滚动页面加载更多商品
            self.scroll_to_load_products()

            products = []
            for i in range(1, max_items + 1):
                try:
                    # 商品链接
                    item = self.driver.find_element(By.XPATH, f'//*[@id="J_goodsList"]/ul/li[{i}]')

                    # 商品ID
                    link = item.find_element(By.CSS_SELECTOR, '.p-img a').get_attribute('href')
                    product_id = re.search(r'/(\d+).html', link).group(1)

                    # 价格
                    try:
                        price = item.find_element(By.CSS_SELECTOR, '.p-price strong i').text
                    except:
                        price = "无价格信息"

                    # 商品名称
                    try:
                        name = item.find_element(By.CSS_SELECTOR, '.p-name em').text
                    except:
                        name = "无商品名称"

                    # 店铺名称
                    try:
                        shop = item.find_element(By.CSS_SELECTOR, '.p-shop span a').text
                    except:
                        shop = "自营"

                    products.append({
                        'id': product_id,
                        'name': name,
                        'price': price,
                        'shop': shop
                    })
                except NoSuchElementException:
                    break
                except Exception as e:
                    print(f"解析商品{i}出错: {str(e)}")

            return products
        except Exception as e:
            print(f"搜索商品出错: {str(e)}")
            return []

    def scroll_to_load_products(self):
        """滚动页面以加载更多商品"""
        scroll_script = """
            window.scrollTo(0, document.body.scrollHeight/3);
            setTimeout(function() {
                window.scrollTo(0, document.body.scrollHeight*2/3);
                setTimeout(function() {
                    window.scrollTo(0, document.body.scrollHeight);
                }, 800);
            }, 800);
        """
        self.driver.execute_script(scroll_script)
        time.sleep(2.5)

    def fetch_comments(self, product, max_pages=10):
        comments = []
        try:
            for page in range(0, max_pages):
                if not self.running:
                    break

                url = f'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc' \
                      f'&clientVersion=1.0.0&t={int(time.time() * 1000)}&loginType=3&productId={product["id"]}' \
                      f'&score=0&sortType=5&page={page}&pageSize=10&isShadowSku=0&fold=1'

                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    if response.status_code != 200:
                        continue

                    data = response.json()
                    if 'comments' not in data:
                        break

                    for comment in data['comments']:
                        comments.append({
                            'product_id': product['id'],
                            'user_id': comment.get('id', ''),
                            'content': comment.get('content', ''),
                            'creation_time': comment.get('creationTime', ''),
                            'location': comment.get('location', ''),
                            'score': comment.get('score', ''),
                            'product_info': {
                                'name': product['name'],
                                'price': product['price'],
                                'shop': product['shop']
                            }
                        })

                    # 如果没有更多评论了
                    if not data.get('comments') or len(data['comments']) < 10:
                        break

                    # 避免请求过快
                    time.sleep(random.uniform(0.5, 1.5))
                except Exception as e:
                    print(f"获取评论出错: {str(e)}")
                    time.sleep(2)
        except Exception as e:
            print(f"获取商品评论出错: {str(e)}")

        return comments

    def save_to_csv(self, filename, data):
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                fieldnames = ['用户id', '品牌', '型号', '店铺', '评论发布时间', '地区', '价格', '评分', '评论']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for comment in data:
                    writer.writerow({
                        '用户id': comment['user_id'],
                        '品牌': '',  # 品牌信息需要从商品名称中提取
                        '型号': comment['product_info']['name'],
                        '店铺': comment['product_info']['shop'],
                        '评论发布时间': comment['creation_time'],
                        '地区': comment['location'],
                        '价格': comment['product_info']['price'],
                        '评分': comment['score'],
                        '评论': comment['content']
                    })
            return True
        except Exception as e:
            print(f"保存文件出错: {str(e)}")
            return False

    def close(self):
        self.running = False
        self.driver.quit()


class JDGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('京东数据获取程序')
        self.root.geometry("800x600+300+100")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.crawler = None
        self.running = False

        self.setup_ui()

    def setup_ui(self):
        # 标题
        tk.Label(self.root, text='京东商品评论爬取工具', font=('Arial', 16)).pack(pady=10)

        # 输入框框架
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill='x', padx=20, pady=10)

        # 关键词输入
        tk.Label(input_frame, text='搜索关键词（多个用逗号分隔）:', anchor='w').grid(row=0, column=0, sticky='w')
        self.keyword_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.keyword_var, width=50).grid(row=0, column=1, sticky='ew', padx=10)

        # 商品数量
        tk.Label(input_frame, text='爬取商品数量:').grid(row=1, column=0, sticky='w', pady=10)
        self.item_count_var = tk.IntVar(value=5)
        tk.Entry(input_frame, textvariable=self.item_count_var, width=10).grid(row=1, column=1, sticky='w', padx=10)

        # 评论页数
        tk.Label(input_frame, text='每商品评论页数:').grid(row=2, column=0, sticky='w')
        self.page_count_var = tk.IntVar(value=10)
        tk.Entry(input_frame, textvariable=self.page_count_var, width=10).grid(row=2, column=1, sticky='w', padx=10)

        # 按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill='x', padx=20, pady=10)

        self.start_btn = tk.Button(button_frame, text='开始爬取', command=self.start_crawling, bg='#4CAF50', fg='white')
        self.start_btn.pack(side='left', padx=5)

        self.stop_btn = tk.Button(button_frame, text='停止爬取', command=self.stop_crawling, state='disabled',
                                  bg='#F44336', fg='white')
        self.stop_btn.pack(side='left', padx=5)

        # 日志输出
        tk.Label(self.root, text='运行日志:').pack(anchor='w', padx=20)
        self.log_area = scrolledtext.ScrolledText(self.root, height=15)
        self.log_area.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        self.log_area.configure(state='disabled')

    def log(self, message):
        self.log_area.configure(state='normal')
        self.log_area.insert('end', f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        self.log_area.see('end')
        self.log_area.configure(state='disabled')

    def start_crawling(self):
        if self.running:
            return

        self.running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')

        keywords = [k.strip() for k in self.keyword_var.get().split(',')]
        max_items = self.item_count_var.get()
        max_pages = self.page_count_var.get()

        if not keywords:
            self.log("请输入关键词!")
            self.running = False
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            return

        self.log("=" * 50)
        self.log(f"开始爬取任务: 关键词={', '.join(keywords)}, 商品数={max_items}, 评论页数={max_pages}")

        # 启动爬虫线程
        threading.Thread(target=self.run_crawler, args=(keywords, max_items, max_pages), daemon=True).start()

    def stop_crawling(self):
        self.running = False
        if self.crawler:
            self.crawler.running = False
        self.log("爬取任务已停止")
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')

    def run_crawler(self, keywords, max_items, max_pages):
        try:
            self.crawler = JDCrawler()
            self.log("正在初始化浏览器...")

            if not self.crawler.login():
                self.log("登录失败或超时，请重试")
                self.running = False
                return

            self.log("登录成功，开始爬取...")

            all_comments = []
            for keyword in keywords:
                if not self.running:
                    break

                self.log(f"搜索关键词: {keyword}")
                products = self.crawler.search_products(keyword, max_items)

                if not products:
                    self.log(f"未找到关键词 '{keyword}' 的商品")
                    continue

                self.log(f"找到 {len(products)} 个商品，开始爬取评论...")

                # 多线程爬取评论
                threads = []
                results = []

                def worker(product):
                    comments = self.crawler.fetch_comments(product, max_pages)
                    with self.lock:
                        results.extend(comments)
                        self.log(f"商品 {product['id']} 爬取完成，获取 {len(comments)} 条评论")

                for product in products:
                    if not self.running:
                        break
                    t = threading.Thread(target=worker, args=(product,))
                    t.start()
                    threads.append(t)
                    # 控制并发数
                    if len(threads) >= 3:
                        for t in threads:
                            t.join()
                        threads = []

                # 等待剩余线程完成
                for t in threads:
                    t.join()

                all_comments.extend(results)

            if all_comments:
                filename = f"JD_Comments_{time.strftime('%Y%m%d%H%M%S')}.csv"
                if self.crawler.save_to_csv(filename, all_comments):
                    self.log(f"数据保存成功: {filename}")
                else:
                    self.log("数据保存失败")
            else:
                self.log("未获取到任何评论数据")

            self.log("爬取任务完成")
        except Exception as e:
            self.log(f"爬取过程中出错: {str(e)}")
        finally:
            if self.crawler:
                self.crawler.close()
            self.running = False
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')

    def on_closing(self):
        if self.running:
            self.stop_crawling()
        self.root.destroy()


if __name__ == '__main__':
    app = JDGUI()
    app.root.mainloop()
