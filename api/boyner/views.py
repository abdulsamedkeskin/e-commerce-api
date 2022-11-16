from flask import Blueprint, request
import cloudscraper
from bs4 import BeautifulSoup
from ..constants import user_agent

boyner = Blueprint("boyner", __name__, url_prefix="/boyner")

@boyner.route("/search", methods=['POST'])
def search():
    scraper = cloudscraper.create_scraper(browser=user_agent)
    q = request.get_json().get("q")
    req = scraper.get(f"https://www.boyner.com.tr/search?q={q}")
    soup = BeautifulSoup(req.content, 'html.parser')
    container = soup.find_all("div", {"class": "product-list-item"})
    results = []
    for i in container:
        name = i.find("span",{"class":"product-name"}).text
        price = i.find("div", {"class": "price-list"})
        price = price.text.replace("\n", "")
        image = i.find("img", {"class": "lazy"})['data-original']
        link = i.find("a", {"class": "ecommerceClick"})['href']
        link = "https://www.boyner.com.tr" + link
        try:
            price = price.lower().split("sepette")[1]
        except:
            price = price        
        results.append({"name": name, "price": price, "img": image,"url": link})
    return results