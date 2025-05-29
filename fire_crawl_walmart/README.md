# Walmart Review Scraper / 沃尔玛评论爬虫

[English](#english) | [中文](#chinese)

<a name="english"></a>
## English

### Introduction
This project is a web scraper designed to extract product reviews from Walmart's website. It uses the Firecrawl API to handle the web scraping process and provides structured data output in CSV format.

### Features
- Extracts detailed review information including:
  - Rating (1-5 stars)
  - Review date
  - Reviewer name
  - Review title
  - Review content
  - Verified purchase status
  - Product color (if available)
  - Helpful votes count
- Supports multi-page scraping
- Saves raw HTML for reference
- Exports data to CSV format
- Handles different review layouts

### Requirements
- Python 3.7+
- firecrawl-py
- beautifulsoup4
- python-dotenv

### Installation
1. Clone the repository
2. Install required packages:
   ```bash
   pip install firecrawl-py beautifulsoup4 python-dotenv
   ```
3. Copy `.env.example` to `.env` and add your Firecrawl API key:
   ```
   FIRECRAWL_API_KEY=your_api_key_here
   ```

### Usage
1. Set up your environment variables in `.env`
2. Run the script:
   ```bash
   python get_content_from_walmart.py
   ```
3. The script will:
   - Scrape reviews from the specified product
   - Save HTML content for each page
   - Generate a CSV file with all reviews

### Output
- HTML files: `walmart-review-page{page}-{random_number}.html`
- CSV file: `walmart_reviews_{product_id}_{timestamp}.csv`

### Disclaimer
This script is for educational and research purposes only. Users must:
- Comply with Walmart's Terms of Service and robots.txt rules
- Use the script responsibly and ethically
- Not use the script for any commercial purposes
- Understand that the author assumes no responsibility for any misuse of this script

---

<a name="chinese"></a>
## 中文

### 项目介绍
这是一个用于抓取沃尔玛网站产品评论的爬虫项目。项目使用 Firecrawl API 处理网页抓取过程，并将数据以CSV格式结构化输出。

### 功能特点
- 提取详细的评论信息，包括：
  - 评分（1-5星）
  - 评论日期
  - 评论者名称
  - 评论标题
  - 评论内容
  - 已验证购买状态
  - 产品颜色（如果有）
  - 点赞数量
- 支持多页评论抓取
- 保存原始HTML以供参考
- 导出CSV格式数据
- 处理不同的评论布局

### 环境要求
- Python 3.7+
- firecrawl-py
- beautifulsoup4
- python-dotenv

### 安装步骤
1. 克隆仓库
2. 安装所需包：
   ```bash
   pip install firecrawl-py beautifulsoup4 python-dotenv
   ```
3. 复制 `.env.example` 到 `.env` 并添加你的 Firecrawl API key：
   ```
   FIRECRAWL_API_KEY=你的API密钥
   ```

### 使用方法
1. 在 `.env` 中设置环境变量
2. 运行脚本：
   ```bash
   python get_content_from_walmart.py
   ```
3. 脚本将会：
   - 抓取指定产品的评论
   - 保存每页的HTML内容
   - 生成包含所有评论的CSV文件

### 输出文件
- HTML文件：`walmart-review-page{页码}-{随机数}.html`
- CSV文件：`walmart_reviews_{产品ID}_{时间戳}.csv`

### 免责声明
本脚本仅用于教育和科学研究目的。使用者必须：
- 遵守沃尔玛的服务条款和robots.txt规则
- 负责任且合乎道德地使用本脚本
- 不得将本脚本用于任何商业目的
- 理解作者对脚本的任何滥用不承担责任 