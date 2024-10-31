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
- ChromeDriver (与Chrome版本匹配)


3. 配置说明 | Configuration
设置要爬取的公众号列表
account_list = ['公众号名称1', '公众号名称2']

3. 运行爬虫 | Run Crawler

4. 输出说明 | Output
- 程序会为每个公众号创建一个CSV文件
- CSV文件包含文章标题、链接和Markdown格式的内容
- 文件名格式：`公众号名称.csv`

## 注意事项 | Notes

- 首次运行需要扫码登录微信
- 登录信息会保存在 account_cookie.txt 中
- 请确保 ChromeDriver 的版本与 Chrome 浏览器版本匹配
- 建议使用代理IP，避免被封禁
- 爬取过程中请勿关闭程序，以免数据丢失



