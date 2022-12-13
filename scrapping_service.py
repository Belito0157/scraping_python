import requests
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w")

class ScrappingService():

    def __init__(self):

        self.base_url = "https://webscraper.io/"
        self.headers = {
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42"
        }
        self.path = "C:/Users/belit/Pictures/chromedriver"

    def scrape_page(self, page_url):
        logging.info(f"Started scrapping the page {page_url}...")
        r = requests.get(page_url)
        if(r.status_code == 200):
            scrapped_page = BeautifulSoup(r.content, 'lxml')
            logging.info(f"Finished scrapping of the page {page_url}.")
            return scrapped_page
        else:
            logging.error(f"Error happend on the server side, response code: {r.status_code}")
            raise Exception(f"Error happend on the server side, response code: {r.status_code}.")

    def get_links_to_all_pages(self):
        logging.info("Getting links to all pages.")
        page_url = self.base_url + "test-sites/e-commerce/allinone/computers/laptops"
        scrapped_page = self.scrape_page(page_url)
        all_pages = scrapped_page.find_all('div', class_='caption')

        all_pages_links = []

        for page in all_pages:
            for link in page.find_all('a', href=True):
                all_pages_links.append(self.base_url + link['href'])
        logging.info("Finished getting links to all pages.")

        return all_pages_links

    def scrape_all_laptops(self, product_name):

        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(self.path, options=op)
        
        logging.info(f"Getting all the laptops of brand {product_name}")
        laptops= []
        all_pages_links = self.get_links_to_all_pages()
        


        for link in all_pages_links:
            lista_preco =[]
            logging.info(f"Started scrapping the page {link}...")
            scrapped_page = self.scrape_page(link)
            logging.info(f"Finished scrapping of the page {link}.")
            driver.get(link)
            
            buttons = driver.find_elements_by_xpath("//button[contains(@class, 'btn swatch')]")

            for button in buttons:
                driver.execute_script("arguments[0].click();", button)
                hdd = driver.find_element_by_xpath("//button[contains(@class, 'btn-primary')]").text                
                valor_texto = driver.find_element_by_tag_name('h4').text
                valor_float = float(valor_texto.replace('$', ''))
                faxu = {hdd+'GB': valor_float}
                lista_preco.append(faxu)
                               

            try:
                name = scrapped_page.find('h4', class_=None).text
            except:
                name = "No name"
                logging.warning("The name of this product is not available")
            try:    
                description = scrapped_page.find('p', class_="description").text
            except:
                description = "No description"
                logging.warning("The description of this product is not available")
            try:
                review = scrapped_page.select('p', class_=None)[5].text.strip()
            except:
                review = "0"
                logging.warning("The reviews of this product are not available")
        
            laptop = {
                'name': name,
                'price': lista_preco,
                'description': description,
                'reviews': review
            }
            print(laptop)
            laptops.append(laptop)

            
        
        laptops = [laptop for laptop in laptops if product_name in laptop['name']]
        logging.info(f"Getting all the laptops of brand {product_name}")
        

        return laptops
