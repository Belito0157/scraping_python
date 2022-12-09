import requests
from bs4 import BeautifulSoup


class ScrappingService():

    def __init__(self):

        self.base_url = "https://webscraper.io/"
        self.headers = {
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42"
        }

    def scrape_page(self, page_url):
        print(f"Started scrapping the page {page_url}...")
        r = requests.get(page_url)
        scrapped_page = BeautifulSoup(r.content, 'lxml')
        print(f"Finished scrapping of the page {page_url}.")

        return scrapped_page

    def get_links_to_all_pages(self):
        print("Getting links to all pages.")
        page_url = self.base_url + "test-sites/e-commerce/allinone/computers/laptops"
        scrapped_page = self.scrape_page(page_url)
        all_pages = scrapped_page.find_all('div', class_='caption')

        all_pages_links = []

        for page in all_pages:
            for link in page.find_all('a', href=True):
                all_pages_links.append(self.base_url + link['href'])
        print("Finished getting links to all pages.")

        return all_pages_links

    def scrape_all_laptops(self, product_name):
        print(f"Getting all the laptops of brand {product_name}")
        laptops= []
        all_pages_links = self.get_links_to_all_pages()


        for link in all_pages_links:
            print(f"Started scrapping the page {link}...")
            scrapped_page = self.scrape_page(link)
            print(f"Finished scrapping of the page {link}.")

            try:
                price = scrapped_page.find('h4', class_="pull-right price").text 
            except:
                price = "0"
            try:
                name = scrapped_page.find('h4', class_=None).text
            except:
                name = "No name"
            try:    
                description = scrapped_page.find('p', class_="description").text
            except:
                description = "No description"
            try:
                review = scrapped_page.select('p', class_=None)[5].text.strip()
            except:
                review = "0"
            try:
                items = [i.text for s in ['button.btn.swatch', 'button.btn.primary'] for i in scrapped_page.select(s)]
            except:
                items=[]
            laptop = {
                'name': name,
                'price': float(price.replace('$', '')),
                'description': description,
                'reviews': review,
                'hdd': items
            }

            laptops.append(laptop)

        laptops = [laptop for laptop in laptops if product_name in laptop['name']]
        print(f"Getting all the laptops of brand {product_name}")

        return sorted(laptops, key=lambda d: d['price']) 
