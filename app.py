from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

BASE_LINK = "https://tiki.vn/may-anh/c1801?src=c.1801.hamburger_menu_fly_out_banner"
def load_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    return soup
def parse_html(url):
    soup = load_url(BASE_LINK)
    soup_item_list = soup.find_all('div', class_ = "product-item")
    item_list = []
    for soup_item in soup_item_list:
        dict_item = {"title":"","link":"","img_url":"","description":"","price":""}
        try:
            dict_item["title"] = soup_item["data-title"]
            dict_item["img_url"] = soup_item.img["src"]
            dict_item["price"] = soup_item.find("span", class_="price-regular").text
            item_list.append(dict_item)
        except:
            pass
    return item_list

def convert_2d(items):
    item_lists = []
    while len(items)>2:
        item_lists.append(items[0:3])
        items = items[3:]
    return item_lists

@app.route('/sendo')
def toShopee():
    data = parse_html(BASE_LINK)
    data = convert_2d(data)
    return render_template('sendo.html',data = data[:3])

@app.route('/')
@app.route('/tiki')
def index():
    data = parse_html(BASE_LINK)
    data = convert_2d(data)
    return render_template('index.html', data = data[:3])

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)