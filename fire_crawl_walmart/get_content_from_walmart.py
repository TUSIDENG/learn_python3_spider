# DISCLAIMER / 免责声明
# This script is for educational and research purposes only.
# The users should comply with Walmart's Terms of Service and robots.txt rules.
# The author assumes no responsibility for any misuse of this script.
# 本脚本仅用于教育和科学研究目的。
# 使用者应遵守Walmart的服务条款和robots.txt规则。
# 作者对脚本的任何滥用不承担责任。

# Install with pip install firecrawl-py
import asyncio
import random
import csv
import os
from bs4 import BeautifulSoup
from firecrawl import AsyncFirecrawlApp
from datetime import datetime
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()


async def extract_reviews(soup):
    """Extract all reviews from the page."""
    reviews = []
    try:
        # Find all review sections - first review has different class
        first_review = soup.find('div', {'class': 'overflow-visible b--none mt3-l ma0 dark-gray'})
        other_reviews = soup.find_all('div', {'class': 'overflow-visible b--none mt4-l ma0 dark-gray'})
        
        # Combine first review with other reviews
        review_sections = [first_review] if first_review else []
        review_sections.extend(other_reviews)
        
        for section in review_sections:
            if not section:  # Skip if section is None
                continue
                
            review = {}
            
            # Extract rating
            rating_div = section.find('div', {'class': 'w_ExHd'})
            if rating_div:
                # 找到所有星星
                all_stars = rating_div.find_all('svg', {'class': ['w_D5ag', 'w_6H0I']})
                rating = 0
                for star in all_stars:
                    # 检查星星的类，w_1jp4表示亮星，w_eDrS表示暗星
                    if 'w_1jp4' in star.get('class', []):
                        rating += 1
                review['rating'] = rating
            else:
                review['rating'] = 0
            
            # Extract review date
            try:
                # 尝试多种可能的日期选择器
                date_div = None
                # 方法1：直接查找日期div
                date_div = section.find('div', {'class': 'f7 gray flex flex-auto flex-none-l tr tl-l justify-end justify-start-l'})
                
                # 方法2：如果方法1失败，查找包含日期的父div
                if not date_div:
                    date_container = section.find('div', {'class': 'flex justify-between items-center self-stretch self-start-m'})
                    if date_container:
                        date_div = date_container.find('div', {'class': 'f7 gray'})
                
                # 提取日期文本
                if date_div:
                    date_text = date_div.get_text(strip=True)
                    review['date'] = date_text
                else:
                    review['date'] = 'N/A'
            except Exception as e:
                print(f"Error extracting date: {e}")
                review['date'] = 'N/A'
            
            # Extract reviewer name
            reviewer_div = section.find('span', {'class': 'f7 b mv0'})
            if reviewer_div:
                review['reviewer'] = reviewer_div.get_text(strip=True)
            else:
                review['reviewer'] = 'Anonymous'
            
            # Extract review title
            title_element = section.find('h3', {'class': 'w_kV33 w_Sl3f w_mvVb f5 b'})
            if title_element:
                review['title'] = title_element.get_text(strip=True)
            else:
                review['title'] = ''
            
            # Extract review content
            content_span = section.find('span', {'class': 'tl-m db-m'})
            if content_span:
                review['content'] = content_span.get_text(strip=True)
            else:
                review['content'] = ''
            
            # Extract verified purchase status
            verified = section.find('span', {'class': 'b f7 dark-gray'})
            if verified and 'Verified Purchase' in verified.get_text():
                review['verified_purchase'] = True
            else:
                review['verified_purchase'] = False
            
            # Extract color information if available
            # @todo 颜色提取待处理
            color_parent = section.find('div', {'class': 'flex f7 items-start content-start self-stretch flex-wrap mt1'})
            if color_parent:
                color_div = color_parent.find('div', {'class': 'flex'})
                if color_div and 'Color' in color_div.get_text():
                    color_text = color_div.get_text(strip=True)
                    review['color'] = color_text.split(':')[1].strip()
                else:
                    review['color'] = ''
            else:
                review['color'] = ''
            
            # Extract helpful votes
            helpful_buttons = section.find_all('button', {'class': 'flex items-center sans-serif ph2 b--none bg-transparent pointer'})
            if helpful_buttons:
                for button in helpful_buttons:
                    if 'thumbsUp' in str(button):
                        votes = button.find('span', {'class': 'ml1 f7 dark-gray'})
                        if votes:
                            review['helpful_votes'] = votes.get_text().strip('()')
                            break
            if 'helpful_votes' not in review:
                review['helpful_votes'] = '0'
            
            reviews.append(review)
            
    except Exception as e:
        print(f"Error extracting reviews: {e}")
    
    return reviews


async def scrape_reviews_page(app, product_id, page=1):
    """Scrape a single page of reviews."""
    base_url = f"https://www.walmart.com/reviews/product/{product_id}?entryPoint=viewAllReviewsBottom"
    url = f"{base_url}&page={page}" if page > 1 else base_url
    
    response = await app.scrape_url(
        url=url,
        formats=['html'],
    )
    
    # Save HTML content with random number
    random_num = random.randint(1000, 9999)
    filename = f'walmart-review-page{page}-{random_num}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.html)
    print(f'HTML content saved to {filename}')
    
    # Parse HTML and extract reviews
    soup = BeautifulSoup(response.html, 'html.parser')
    return await extract_reviews(soup)


def save_reviews_to_csv(reviews, product_id):
    """Save reviews to a CSV file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'walmart_reviews_{product_id}_{timestamp}.csv'
    
    # Define CSV headers
    headers = [
        'rating', 
        'date', 
        'reviewer', 
        'title', 
        'content', 
        'verified_purchase',
        'color',
        'helpful_votes'
    ]
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for review in reviews:
                writer.writerow(review)
        print(f"\nReviews have been saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


async def main():
    # 从环境变量获取API key
    api_key = os.getenv('FIRECRAWL_API_KEY')
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY not found in .env file")
        
    app = AsyncFirecrawlApp(api_key=api_key)
    product_id = "432328045"
    
    # Get reviews from multiple pages
    all_reviews = []
    for page in range(1, 4):  # Get first 3 pages
        page_reviews = await scrape_reviews_page(app, product_id, page)
        all_reviews.extend(page_reviews)
    reviews = all_reviews
    
    # Save reviews to CSV
    save_reviews_to_csv(reviews, product_id)
    
    # Print reviews in a formatted way
    print(f"\nProduct Reviews (Total: {len(reviews)} reviews):")
    print("-" * 50)
    
    for i, review in enumerate(reviews, 1):
        print(f"\nReview #{i}")
        print("-" * 20)
        print(f"Rating: {'★' * review.get('rating', 0)}")
        print(f"Date: {review.get('date', 'N/A')}")
        print(f"Reviewer: {review.get('reviewer', 'Anonymous')}")
        if review.get('title'):
            print(f"Title: {review['title']}")
        print(f"Content: {review.get('content', 'N/A')}")
        print(f"Verified Purchase: {'Yes' if review.get('verified_purchase') else 'No'}")
        if review.get('color'):
            print(f"Color: {review['color']}")
        print(f"Helpful Votes: {review.get('helpful_votes', '0')}")


if __name__ == "__main__":
    asyncio.run(main())