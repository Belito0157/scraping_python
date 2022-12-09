from scrapping_service import ScrappingService 

class Test():
    scrapping_service = ScrappingService()

    laptops = scrapping_service.scrape_all_laptops("Lenovo")

    print(laptops)