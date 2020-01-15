import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
from random import uniform

csv_file = "scraping_proj.csv"

with open(csv_file, "w") as f:

    # Establish base blog url and csv headers
    base_url = "https://www.rithmschool.com"
    blog_url = "https://www.rithmschool.com/blog"
    headers = ['Title', 'Date', 'URL']

    # Write CSV headers
    csv_writer = csv.DictWriter(f, fieldnames=headers)
    csv_writer.writeheader()

    # Loop through blog, breaking out once articles on last page have been scraped.
    while True:
        # Pull HTML with Beautiful Soup
        response = requests.get(blog_url)
        soup = BeautifulSoup(response.text, "html.parser")

        # last_page flag determines if we are on the last available page
        last_page = False

        # If we are on the last page, set last_page to True
        try:
            next_page = soup.find(class_="next").find("a")['href']
        except AttributeError:
            last_page = True

        # Find articles on page
        articles = soup.find_all("article")
        print(f'Searching page {blog_url}')

        # Loop through each article tag on page, collecting url,date,title
        for article in articles:
            a_tag = article.find("a")
            title = a_tag.get_text()
            url = f"https://www.rithmschool.com{a_tag.attrs['href']}"
            date = article.find("time")['datetime']
            csv_writer.writerow({'Title': title, 'Date': date, 'URL': url})

        # After collecting articles, if we are on the last page, break out.
        # Else, update blog_url with next page.

        if last_page:
            print("Last page reached. Terminating.")
            break
        else:
            # Update blog_url with url of next blog page
            blog_url = f"{base_url}{next_page}"

            # Pause for 5-7s before next page request
            sleep_time = uniform(5.0, 7.0)
            print(f"Sleeping for {round(sleep_time,2)} seconds")
            sleep(sleep_time)
