import requests
from bs4 import BeautifulSoup
import csv
import schedule
import time

def crawl_and_save(url, output_file):
    try:
        # Thực hiện yêu cầu HTTP
        response = requests.get(url)
        response.raise_for_status()  # Nếu có lỗi HTTP, raise một exception

        # Kiểm tra nội dung của trang web
        if 'text/html' not in response.headers['content-type']:
            raise ValueError('The content is not HTML')

        # Parse HTML bằng BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Tìm và in URL của trang web
        webpage_url = response.url
        print(f"Webpage URL: {webpage_url}\n")

        # Mở hoặc tạo tệp cho việc ghi dữ liệu vào CSV
        with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Ghi dòng header
            csv_writer.writerow(['Title', 'Link Article', 'Content', 'Link Image'])

            # Trích xuất và ghi tiêu đề với liên kết, nội dung và liên kết hình ảnh
            for h3 in soup.find_all('h3'):
                h3_text = h3.text.strip()

                # Tìm thẻ mở đầu (anchor tag) đầu tiên trong h3 (giả sử có)
                a_tag = h3.find('a')
                if a_tag:
                    title_link = a_tag['href']

                    # Tìm thẻ p tiếp theo (giả sử có)
                    p_tag = h3.find_next('p')
                    if p_tag:
                        content_text = p_tag.text.strip()

                        # Tìm thẻ hình ảnh đầu tiên trong cùng cha với h3
                        img_tag = h3.find_parent().find('img', attrs={'src': True})
                        if img_tag:
                            image_link = img_tag['src']

                            # Ghi dòng vào tệp CSV
                            csv_writer.writerow([h3_text, title_link, content_text, image_link])

                            # In thông tin
                            print(f"Title: {h3_text}\nLink Article: {title_link}\nContent: {content_text}\nLink Image: {image_link}\n")

    except requests.RequestException as req_ex:
        print(f"HTTP request error: {req_ex}")
    except Exception as ex:
        print(f"An error occurred: {ex}")

# Hàm chạy công việc crawl
def job_crawl():
    try:
        print("Crawling job started...")
        url_to_crawl = 'https://vnexpress.net/tin-tuc-24h'
        output_file_path = 'data_crawl.csv'
        crawl_and_save(url_to_crawl, output_file_path)
        print("Crawling job completed successfully.")
    except Exception as e:
        print(f"An error occurred during crawling: {e}")

# Thực hiện công việc crawl ngay từ đầu
job_crawl()

# Lên lịch chạy công việc crawl mỗi giờ
schedule.every().hour.do(job_crawl)

# Chạy lịch trình
while True:
    try:
        schedule.run_pending()
        time.sleep(60)  # Đặt thời gian nghỉ là 60 giây
    except KeyboardInterrupt:
        print("Scheduler stopped by user.")
        break
    except Exception as e:
        print(f"An error occurred in the scheduler: {e}")
