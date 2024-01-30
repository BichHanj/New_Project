import requests
from bs4 import BeautifulSoup
import schedule
import time

def crawl_static_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract and print the URL of the webpage
            webpage_url = response.url
            print(f"Webpage URL: {webpage_url}\n")

            # Extract and print titles with links, content, and image links
            for h3 in soup.find_all('h3'):
                h3_text = h3.text.strip()

                # Find the first anchor tag within the h3 (assuming there is one)
                a_tag = h3.find('a')
                if a_tag:
                    title_link = a_tag['href']

                    # Find the next sibling <p> tag (assuming there is one)
                    p_tag = h3.find_next('p')
                    content_text = p_tag.text.strip() if p_tag else None

                    # Find the first image tag within the parent of h3
                    img_tag = h3.find_parent().find('img', attrs={'src': True})
                    image_link = img_tag['src'] if img_tag else None

                    print(f"Title: {h3_text}\nLink: {title_link}\nContent: {content_text}\nImage Link: {image_link}\n")

        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

def job():
    print("I'm working...")
    crawl_static_website('https://vnexpress.net/tin-tuc-24h')

def job_with_argument(name):
    print(f"I am {name}")

# Schedule the crawling job every 10 seconds
schedule.every(10).seconds.do(job)

# Schedule the job with an argument every 5 minutes
schedule.every(5).minutes.do(job_with_argument, name="Peter")

while True:
    schedule.run_pending()
    time.sleep(1)
