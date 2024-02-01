import requests
from bs4 import BeautifulSoup
import csv
import psycopg2
import schedule
import time

db_config = {
    "dbname": "New_project",
    "user": "postgres",
    "password": "baotran123",
    "host": "localhost",
    "port": "5555",
}

def create_table(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_article (
                id SERIAL PRIMARY KEY,
                Title VARCHAR(255),
                "Link Article" VARCHAR(255),
                Content TEXT,
                "Link Image" VARCHAR(255)
            )
        """)
        print("Table created successfully.")
    except Exception as ex:
        print(f"Error creating table in PostgreSQL: {ex}")

def crawl_and_save(url, output_file):
    try:
        
        response = requests.get(url)
        response.raise_for_status()  
        if 'text/html' not in response.headers['content-type']:
            raise ValueError('The content is not HTML')
        soup = BeautifulSoup(response.content, 'html.parser')

        webpage_url = response.url
        print(f"Webpage URL: {webpage_url}\n")
        with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Title', 'Link Article', 'Content', 'Link Image'])
            for h3 in soup.find_all('h3'):
                h3_text = h3.text.strip()
                a_tag = h3.find('a')
                if a_tag:
                    title_link = a_tag['href']
                    p_tag = h3.find_next('p')
                    if p_tag:
                        content_text = p_tag.text.strip()
                        img_tag = h3.find_parent().find('img', attrs={'src': True})
                        if img_tag:
                            image_link = img_tag['src']
                            csv_writer.writerow([h3_text, title_link, content_text, image_link])

                            print(f"Title: {h3_text}\nLink Article: {title_link}\nContent: {content_text}\nLink Image: {image_link}\n")

    except requests.RequestException as req_ex:
        print(f"HTTP request error: {req_ex}")
    except Exception as ex:
        print(f"An error occurred: {ex}")

def insert_data_to_postgres(title, link_article, content, link_image, cursor):
    try:
        cursor.execute("INSERT INTO data_article (Title, \"Link Article\", Content, \"Link Image\") VALUES (%s, %s, %s, %s)",
                       (title, link_article, content, link_image))
    except Exception as ex:
        print(f"Error inserting data to PostgreSQL: {ex}")

def crawl_and_update(url, output_file):
    try:
        crawl_and_save(url, output_file)

        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                create_table(cursor)  
                with open(output_file, 'r', encoding='utf-8') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    next(csv_reader)  # Skip header row
                    for row in csv_reader:
                        title, link_article, content, link_image = row
                        insert_data_to_postgres(title, link_article, content, link_image, cursor)

    except Exception as e:
        print(f"An error occurred during crawl and update: {e}")

def job_crawl_and_update():
    print("Crawling and updating job started...")
    url_to_crawl = 'https://vnexpress.net/tin-tuc-24h'
    output_file_path = 'data_crawl123.csv'
    crawl_and_update(url_to_crawl, output_file_path)
    print("Crawling and updating job completed successfully.")


job_crawl_and_update()

def job_crawl_and_update():
    print("Crawling and updating job started...")
    url_to_crawl = 'https://vnexpress.net/tin-tuc-24h'
    output_file_path = 'data_crawl123.csv'
    crawl_and_update(url_to_crawl, output_file_path)
    print("Crawling and updating job completed successfully.")

# Lịch và vòng lặp chạy lịch
def schedule_crawl_and_update():
    schedule.every(10).minutes.do(job_crawl_and_update)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)  
        except KeyboardInterrupt:
            print("Scheduler stopped by user.")
            break
        except Exception as e:
            print(f"An error occurred in the scheduler: {e}")

job_crawl_and_update()

schedule_crawl_and_update()
