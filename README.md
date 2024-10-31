# WxCrawler

一个用于获取微信公众号文章的爬虫工具。
A crawler tool for WeChat Official Account articles.

## 免责声明 | Disclaimer

1. 本工具仅供学习和研究使用，请勿用于任何商业用途或非法目的。
   This tool is for learning and research purposes only. Commercial use or illegal purposes are strictly prohibited.

2. 使用本工具时请遵守相关法律法规，不得违反微信平台的使用条款和规则。
   Please comply with relevant laws and regulations when using this tool. Do not violate WeChat platform terms and rules.

3. 请合理使用本工具，不要进行过度采集，以免给目标服务器造成不必要的压力。
   Please use this tool reasonably and avoid excessive crawling to prevent unnecessary pressure on target servers.

4. 对于使用本工具所产生的任何直接或间接后果，本项目开发者不承担任何责任。
   The developers of this project are not responsible for any direct or indirect consequences arising from the use of this tool.

5. 使用本工具即表示您已经完全理解并同意上述免责声明。
   By using this tool, you fully understand and agree to the above disclaimer.

## 功能特点 | Features

- 支持微信公众号文章的批量采集
  Support batch collection of WeChat Official Account articles

## 使用说明 | Instructions

1. 安装依赖 | Install Dependencies
- requests
- selenium
- beautifulsoup4
- html2text

2. 环境要求 | Requirements
- Python 3.6+
- Chrome浏览器
- ChromeDriver (与Chrome版本匹配) 下载地址: https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json


3. 配置说明 | Configuration
修改 .env.example 文件，设置要爬取的公众号列表、爬取的文章数量、ChromeDriver路径，然后把 .env.example 文件名修改为 .env 文件


4. 运行爬虫 | Run Crawler

5. 输出说明 | Output
- 程序会为每个公众号创建一个CSV文件
- CSV文件包含文章标题、链接和Markdown格式的内容
- 文件名格式：`公众号名称.csv`

## 注意事项 | Notes

- 每次运行需要扫码登录微信
- 登录信息会保存在 account_cookie.txt 中
- 请确保 ChromeDriver 的版本与 Chrome 浏览器版本匹配
- 建议使用代理IP，避免被封禁
- 爬取过程中请勿关闭程序，以免数据丢失

## 开源协议 | License

本项目采用 MIT 协议开源。
This project is open-sourced under the MIT License.

Copyright (c) 2024 WxCrawler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.




This project is open-sourced under the MIT License.

Copyright (c) 2024 WxCrawler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

