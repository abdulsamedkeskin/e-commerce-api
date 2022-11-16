from flask import Blueprint, request
import cloudscraper
from bs4 import BeautifulSoup
from ..constants import user_agent

trendyol = Blueprint("trendyol", __name__, url_prefix="/trendyol")

@trendyol.route("/search", methods=['POST'])
def search():
    scraper = cloudscraper.create_scraper(browser=user_agent)
    q = request.get_json().get("q")
    req = scraper.get(f"https://www.trendyol.com/sr?q={q}")
    soup = BeautifulSoup(req.content, 'html.parser')
    container = soup.find_all("div", {"class": "p-card-wrppr"})
    results = []
    for i in container:
        link = i.find("a")['href']
        link = "https://www.trendyol.com" + link
        brand_name = i.find("span", {"class": "prdct-desc-cntnr-ttl"}).text
        product_name = i.find("span", {"class": "prdct-desc-cntnr-name"}).text
        price = i.find("div", {"class": "prc-box-dscntd"}).text
        results.append({"product_name": product_name,"brand_name": brand_name,"price": price,"url": link})
    return results