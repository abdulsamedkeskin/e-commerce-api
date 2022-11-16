from flask import Blueprint, request
from bs4 import BeautifulSoup
from ..constants import user_agent
import cloudscraper
google = Blueprint("google", __name__, url_prefix="/google")

@google.route("/search", methods=['POST'])
def search():
    scraper = cloudscraper.create_scraper(browser=user_agent)
    q = request.get_json().get("q")
    req = scraper.get(f"https://www.google.com/search?q={q}&tbm=shop")
    soup = BeautifulSoup(req.content, 'html.parser')
    container = soup.find("div", {"id": "rso"})
    try:
        container = container.find_all("div", {"class": "Qlx7of"})
    except AttributeError:
        return {"status": 404,"message": "not found"}, 404
    results = []
    for i in container:
        wrapper = i.find("div", {"class":"sh-pr__product-results"})
        wrapper = wrapper.find_all("div", {"class": "sh-dgr__grid-result"})
        for _ in wrapper:
            link = _.find("a", {"class":"xCpuod"})
            try:
                product_id = link['href'].split("/shopping/product/")[1].split("?")[0]
                name = _.find("h3", {"class": "tAxDx"}).text
            except:
                continue
            results.append({"name": name,"product_id": product_id}) 
    return results, 200

@google.route("/search/<product_id>", methods=['GET'])
def search_by_product_id(product_id):
    scraper = cloudscraper.create_scraper(browser=user_agent)
    req = scraper.get(f"https://www.google.com/shopping/product/{product_id}/offers")
    soup = BeautifulSoup(req.content, 'html.parser')
    product_name = soup.find("title").text.split(" | Google")[0]
    container = soup.find("div", {"id": "sh-oo__offers-grid-wrapper"})
    try:
        container = container.find("tr",{"class":"sh-osd__offer-row"}).parent
    except:
        return {"status": 404, "message": "not found"}, 404
    results = []
    for i in container:
        price = i.find("span", {"class": "g9WBQb"})
        link = i.find("a", {"rel": "noopener"})
        try:
            name = link.text.split("Y")[0]
            link = link['href'].split("/url?q=")[1]
            price = price.text
        except:
            continue
        results.append({"product_name": product_name,"name": name, "price": price,"url": link})
    return sorted(results, key=lambda x: x['price']), 200