import requests
from bs4 import BeautifulSoup

def next_page(base_url, blog_url):
    try:
        response = requests.get(blog_url).text
        soup = BeautifulSoup(response, "html.parser")
        next_page_finder = soup.find(class_="next").find("a")['href']
        return f"{base_url}{next_page_finder}"
    except AttributeError:
        return False
