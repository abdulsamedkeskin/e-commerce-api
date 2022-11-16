from flask import Blueprint, request
import cloudscraper
from bs4 import BeautifulSoup
from ..constants import user_agent

hepsiburada = Blueprint("hepsiburada", __name__, url_prefix="/hepsiburada")

@hepsiburada.route("/search", methods=['POST'])
def search():
    scraper = cloudscraper.create_scraper(browser=user_agent)
    q = request.get_json().get("q")
    req = scraper.get(f"https://www.hepsiburada.com/ara?q={q}")
    soup = BeautifulSoup(req.content, 'html.parser')
    container = soup.find_all("li", {"class": "productListContent-zAP0Y5msy8OHn5z7T_K_"})
    results = []
    for i in container:
        wrapper = i.find("div",{"data-test-id": "product-info-wrapper"})
        title = wrapper.find("h3", {"data-test-id":"product-card-name"})
        price = wrapper.find("div", {"data-test-id": "price-current-price"})
        link = i.find("a")['href']
        link = "https://www.hepsiburada.com" + link
        results.append({"title": title.text, "price": price.text, "link": link})
    return results