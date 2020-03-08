from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)

vatgia_link = 'https://vatgia.com/319/may-anh-so.html'
def get_url(URL):
  r = requests.get(URL)
  soup = BeautifulSoup(r.text, 'html.parser')
  return soup

def get_vatgia(URL):
  soup = get_url(URL)
  l = []
  blocks = soup.find_all('div', {'class':'block no_picture_thumb'})
  block = blocks[0]
  for block in blocks:
    d = {}
    name = block.find('div', {'class':'name'})
    d["name"] = name.a.text
    price = block.find('div', {'class':'price'})
    d['price'] = price.text
    picture = block.find('a', {'class':'picture_link'})
    d['img'] = picture.img['src']
    l.append(d)
  return l

BASE_LINK = "https://tiki.vn/may-anh/c1801?src=c.1801.hamburger_menu_fly_out_banner"
def load_url(url):
    r = requests.get(url)
    return r
def parse_html(url):
    r =  load_url(BASE_LINK)
    soup = BeautifulSoup(r.text,'html.parser')
    soup_item_list = soup.find_all('div', class_ = "product-item")
    item_list = []
    for soup_item in soup_item_list:
        dict_item = {"title":"","link":"","image_url":"","description":"","price":""}
        try:
            dict_item["title"] = soup_item["data-title"]
            dict_item["img_url"] = soup_item.img["src"]
            dict_item["price"] = soup_item.find("span", class_="price-regular").text
            item_list.append(dict_item)
        except:
            pass

#    tikiDeal = tikiDeal.find('div', class_ = "List__Wrapper-sc-6lyqk4-0 layRnl")
    
    return item_list

@app.route('/')
def index():

    data = parse_html(BASE_LINK)
    return render_template('index.html', data = data[:3])

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)