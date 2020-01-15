import requests
from bs4 import BeautifulSoup
import csv
# from page_finder import next_page

csv_file = "colt/scraping/blog_scraping/scraping_proj.csv"

def next_page(base_url, blog_url):
    try:
        response = requests.get(blog_url).text
        soup = BeautifulSoup(response, "html.parser")
        next_page_finder = soup.find(class_="next").find("a")['href']
        return f"{base_url}{next_page_finder}"
    except AttributeError:
        return False

with open(csv_file, "w") as f:
    # Establish base blog url and csv headers
    base_url = "https://www.rithmschool.com"
    blog_url = "https://www.rithmschool.com/blog"
    headers = ['Title', 'Date', 'URL']

    #Write CSV headers
    csv_writer = csv.DictWriter(f, fieldnames=headers)
    csv_writer.writeheader()

    #While a next page exists, scrape articles
    while next_page(base_url, blog_url):
        print(f'searching page {blog_url}')
        response = requests.get(blog_url)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article")

        #Loop through each article tag on page, collecting url,date,title
        for article in articles:
            a_tag = article.find("a")
            title = a_tag.get_text()
            url = f"https://www.rithmschool.com{a_tag.attrs['href']}"
            date = article.find("time")['datetime']
            csv_writer.writerow({'Title':title, 'Date': date, 'URL':url})

        #Update blog_url with url of next blog page
        blog_url = next_page(base_url,blog_url)





# with open(csv_file, "w") as f:
#     headers = ['Title', 'Date', 'URL']
#     csv_writer = csv.DictWriter(f, fieldnames=headers)
#     csv_writer.writeheader()
#     for article in articles:
#         a_tag = article.find("a")
#         title = a_tag.get_text()
#         url = f"https://www.rithmschool.com{a_tag.attrs['href']}"
#         date = article.find("time")['datetime']
#         csv_writer.writerow({'Title':title, 'Date': date, 'URL':url})
