# -*- coding: utf-8 -*-
import json
import time
import random
import csv
import logging
from pathlib import Path
from typing import List, Dict, Optional
import re

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import html2text

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeixinCrawler:
    def __init__(self, account_list: List[str], chrome_driver_path: str = '/usr/local/bin/chromedriver',
                 max_articles: int = 5):
        """
        初始化微信公众号爬虫
        :param account_list: 要爬取的公众号列表
        :param chrome_driver_path: ChromeDriver路径
        :param max_articles: 每个公众号最多取的文章数量，默认为5
        """
        self.account_list = account_list
        self.chrome_driver_path = chrome_driver_path
        self.max_articles = max_articles
        self.cookie_file = Path('account_cookie.txt')
        self.base_url = 'https://mp.weixin.qq.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        self.qrcode_flag = True

    def _init_chrome_driver(self) -> webdriver.Chrome:
        """初始化Chrome浏览器"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        service = Service(self.chrome_driver_path)
        return webdriver.Chrome(service=service, options=chrome_options)

    def _wait_for_cookies(self, browser: webdriver.Chrome, required_cookies: List[str] = None) -> Dict[str, str]:
        """
        等待并获取必要的cookies
        :param browser: Chrome浏览器实例
        :param required_cookies: 必需的cookie列表
        :return: cookie字典
        """
        if required_cookies is None:
            required_cookies = ['ua_id', 'uuid', '_clck']

        max_attempts = 10
        for attempt in range(max_attempts):
            cookies = browser.get_cookies()
            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}

            missing_cookies = [name for name in required_cookies if name not in cookie_dict]

            if not missing_cookies:
                logger.info("已成功获取所有必要的cookies")
                return cookie_dict

            logger.info(f"第 {attempt + 1} 次尝试，还缺少以下cookies: {missing_cookies}")
            if attempt % 2 == 0:
                browser.refresh()
            time.sleep(3)

        raise TimeoutException("无法获取所需的全部cookies")

    def _get_qrcode(self, cookie_dict: Dict[str, str]) -> bool:
        """
        获取登录二维码
        :param cookie_dict: cookie字典
        :return: 是否成功获取二维码
        """
        headers = self.headers.copy()
        headers['Cookie'] = '; '.join([f"{k}={v}" for k, v in cookie_dict.items()])

        random_timestamp = str(int(time.time() * 1000))
        qrcode_url = f'{self.base_url}/cgi-bin/scanloginqrcode?action=getqrcode&random={random_timestamp}'

        try:
            response = requests.get(qrcode_url, headers=headers)
            if response.status_code == 200:
                with open('qrcode.png', 'wb') as f:
                    f.write(response.content)
                logger.info("二维码已保存到 qrcode.png")
                return True
            else:
                logger.error(f"获取二维码失败，状态码: {response.status_code}")
                return False
        except requests.RequestException as e:
            logger.error(f"获取二维码时发生错误: {e}")
            return False

    def get_qrcode_status(self, cookie_dict):
        headers = self.headers.copy()
        headers['Cookie'] = '; '.join([f"{k}={v}" for k, v in cookie_dict.items()])
        url = 'https://mp.weixin.qq.com/cgi-bin/scanloginqrcode?action=ask&token=&lang=zh_CN&f=json&ajax=1'
        data = {
            'action': 'ask',
            'token': '',
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': 1,
        }
        try:
            res = requests.get(url=url, params=data, headers=headers).json()
            if res.get('status') == 0:
                logger.info('未扫码')
            elif res.get('status') == 4:
                logger.info('已扫码')
            elif res.get('status') == 1:
                logger.info('已登录')
                self.qrcode_flag = False
            time.sleep(4)
        except Exception as e:
            logger.error(f'检测二维码状态出错')
            return 'error'

    def login(self) -> bool:
        """
        执行登录流程
        :return: 是否登录成功
        """
        browser = None
        try:
            browser = self._init_chrome_driver()
            logger.info("启动浏览器，打开微信公众号登录界面...")
            browser.get(self.base_url)

            cookie_dict = self._wait_for_cookies(browser)
            if not self._get_qrcode(cookie_dict):
                return False

            logger.info("请在 20 秒内使用微信扫描二维码登录...")
            self.start_time = int(time.time())
            while self.qrcode_flag:
                self.get_qrcode_status(cookie_dict)

            # 保存登录后的cookies
            browser.get(self.base_url)
            cookies = browser.get_cookies()
            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}

            with open(self.cookie_file, 'w', encoding='utf-8') as f:
                json.dump(cookie_dict, f)
            logger.info("登录cookies已保存到本地")

            return True

        except Exception as e:
            logger.error(f"登录过程中发生错误: {e}")
            return False
        finally:
            if browser:
                browser.quit()

    def _get_token(self, cookies: Dict[str, str]) -> Optional[str]:
        """获取token"""
        try:
            response = requests.get(self.base_url, cookies=cookies, headers=self.headers)

            token = re.findall(r'token=(\d+)', str(response.url))[0]
            print(f"token: {token}")
            return token
        except Exception as e:
            logger.error(f"获取token失败: {e}")
            return None

    def _get_account_fakeid(self, account: str, token: str, cookies: Dict[str, str]) -> Optional[str]:
        """
        获取公众号fakeid，更新cookies
        :param account: 公众号名称
        :param token: token
        :param cookies: cookies
        :return: 选中的公众号fakeid
        """
        search_url = f'{self.base_url}/cgi-bin/searchbiz'
        params = {
            'action': 'search_biz',
            'begin': '0',
            'count': '5',
            'query': account,
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
        }

        try:
            response = requests.get(search_url, cookies=cookies, headers=self.headers, params=params)

            # 获取并更新cookies
            new_cookies = response.cookies.get_dict()
            if new_cookies:
                cookies.update(new_cookies)
                # 保存更新后的cookies到本地
                with open(self.cookie_file, 'w', encoding='utf-8') as f:
                    json.dump(cookies, f)
                logger.info("已更新本地cookies")

            account_list = response.json().get('list', [])

            if not account_list:
                logger.error(f"未找到与 '{account}' 相关的公众号")
                return None

            # 打印搜索结果
            logger.info(f"\n找到 {len(account_list)} 个相关公众号:")
            print("\n序号  公众号名称  认证信息  简介")
            print("-" * 50)

            for idx, acc in enumerate(account_list, 1):
                nickname = acc.get('nickname', '未知')
                signature = acc.get('signature', '无')
                verified = "已认证" if acc.get('verified', False) else "未认证"
                print(f"{idx:<4} {nickname:<10} {verified:<6} {signature}")

            # 用户选择
            while True:
                try:
                    choice = input("\n请输入要爬取的公众号序号 (输入 q 退出): ")
                    if choice.lower() == 'q':
                        return None

                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(account_list):
                        selected = account_list[choice_idx]
                        logger.info(f"已选择: {selected['nickname']}")
                        return selected['fakeid']
                    else:
                        print("无效的序号，请重新输入")
                except ValueError:
                    print("请输入有效的数字")
                except KeyboardInterrupt:
                    print("\n已取消选择")
                    return None

        except Exception as e:
            logger.error(f"获取公众号fakeid失败: {e}")
            return None

    def crawl_articles(self, account: str) -> bool:
        """
        爬取指定公众号的文章
        :param account: 公众号名称
        :return: 是否成功爬取
        """
        try:
            # 每次都重新读取cookies，确保使用最新的
            with open(self.cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)

            token = self._get_token(cookies)
            print(f"token: {token}")
            if not token:
                return False

            fakeid = self._get_account_fakeid(account, token, cookies)
            if not fakeid:
                return False

            # 重新读取更新后的cookies
            with open(self.cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)

            return self._save_articles(account, fakeid, token, cookies)

        except Exception as e:
            logger.error(f"爬取文章过程中发生错误: {e}")
            return False

    def _save_articles(self, account: str, fakeid: str, token: str, cookies: Dict[str, str]) -> bool:
        """保存公众号文章"""
        file_name = f'{account}.csv'
        file_head = ['title', 'link', 'content']
        articles_saved = 0  # 记录已保存的文章数量

        try:
            with open(file_name, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, file_head)
                writer.writeheader()

                begin = 0
                while True:
                    articles = self._get_articles_batch(fakeid, token, cookies, begin)
                    if not articles:
                        break

                    for article in articles['list']:
                        if articles_saved >= self.max_articles:
                            logger.info(f"已达到最大文章数量限制: {self.max_articles}")
                            return True

                        try:
                            content = self._get_article_content(article['link'], cookies)
                            article['content'] = content
                            writer.writerow(article)  # 立即写入每篇文章
                            articles_saved += 1
                            logger.info(f"成功获取文章内容 ({articles_saved}/{self.max_articles}): {article['title']}")
                        except Exception as e:
                            logger.error(f"获取文章内容失败: {article['title']}, 错误: {e}")
                            article['content'] = ''

                        time.sleep(random.uniform(2, 4))

                    if articles_saved >= self.max_articles:
                        break

                    begin += 5
                    time.sleep(2)

            logger.info(f"共成功保存 {articles_saved} 篇文章")
            return True

        except Exception as e:
            logger.error(f"保存文章时发生错误: {e}")
            return False

    def _get_articles_batch(self, fakeid: str, token: str, cookies: Dict[str, str], begin: int) -> Optional[Dict]:
        """
        获取一批文章
        :param fakeid: 公众号的fakeid
        :param token: 访问令牌
        :param cookies: cookies
        :param begin: 开始位置
        :return: 包含文章列表和总数的字典
        """
        url = f'{self.base_url}/cgi-bin/appmsgpublish'
        params = {
            'sub': 'list',
            'search_field': None,
            'begin': str(begin),
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '101_1',
            'free_publish_type': '1',
            'sub_action': 'list_ex',
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1'
        }

        try:
            response = requests.get(url, cookies=cookies, headers=self.headers, params=params)
            data = response.json()

            # 添加响应检查和日志
            if 'base_resp' in data and data['base_resp'].get('ret') != 0:
                logger.error(f"获取文章列表失败: {data['base_resp']}")
                return None

            articles = []
            publish_page = eval(data.get('publish_page', {}))

            for page in publish_page.get('publish_list', []):
                # print(f" type of page: {type(page)}, page: {page}")
                if page:
                    publish_info = json.loads(page.get('publish_info', {}))
                    appmsgex = publish_info.get('appmsgex', [])
                    for article in appmsgex:
                        article_data = {
                            'title': article.get('title', ''),
                            'link': article.get('link', ''),
                        }
                        articles.append(article_data)
                        logger.info(f"获取到文章: {article_data['title']}")

            return {
                'list': articles,
                'total': publish_page.get('total_count', 0)  # 更新总数的获取位置
            }

        except requests.RequestException as e:
            logger.error(f"请求文章列表时发生网络错误: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"解析响应JSON时发生错误: {e}")
            return None
        except Exception as e:
            logger.error(f"获取文章批次时发生未知错误: {e}")
            return None

    def _get_article_content(self, url: str, cookies: Dict[str, str]) -> str:
        """
        获取文章内容
        :param url: 文章链接
        :param cookies: cookies字典
        :return: 文章内容
        """
        try:
            # 处理URL中的转义字符
            url = url.replace('\\/', '/')

            # 构建请求头
            headers = self.headers.copy()
            headers['Host'] = 'mp.weixin.qq.com'
            headers['Upgrade-Insecure-Requests'] = '1'

            # 发送请求获取文章内容
            response = requests.get(url, cookies=cookies, headers=headers, timeout=20)
            response.raise_for_status()  # 检查响应状态
            response.encoding = 'utf-8'

            # 使用 BeautifulSoup 解析内容
            soup = BeautifulSoup(response.text, 'html.parser')
            article_element = soup.find(class_="rich_media_content")

            if not article_element:
                logger.error(f"未找到文章内容: {url}")
                return ""

            # 移除脚本和样式
            for script in article_element(["script", "style"]):
                script.decompose()

            # 使用 html2text 转换为 markdown 格式文本
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            text_content = h.handle(str(article_element))

            return text_content.strip()

        except requests.Timeout:
            logger.error(f"请求文章超时: {url}")
            return ""
        except requests.RequestException as e:
            logger.error(f"请求文章失败: {url}, 错误: {e}")
            return ""
        except Exception as e:
            logger.error(f"处理文章内容时发生错误: {url}, 错误: {e}")
            return ""

    def run(self):
        """运行爬虫"""
        if not self.login():
            logger.error("登录失败")
            return

        for account in self.account_list:
            logger.info(f"开始爬取公众号：{account}")
            if self.crawl_articles(account):
                logger.info(f"公众号 {account} 爬取完成")
            else:
                logger.error(f"公众号 {account} 爬取失败")


if __name__ == '__main__':
    # 设置要爬取的公众号列表
    account_list = ['极客时间']

    # 创建爬虫实例并运行
    crawler = WeixinCrawler(account_list, chrome_driver_path='./chromedriver-win64/chromedriver.exe', max_articles=10)
    crawler.run()
