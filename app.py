from flask import Flask, jsonify
from flask_restful import Api, Resource
from scrapping_service import ScrappingService 
import logging

app = Flask(__name__)
api = Api(app)

logging.basicConfig(level=logging.INFO, filename="api.log", filemode="w")

class laptops(Resource):
    def get(self, brand):
        try:
            scrapping_service = ScrappingService()
            laptops = scrapping_service.scrape_all_laptops(brand)
            return jsonify(laptops)
        except Exception as exc:
            raise Exception("Could not scrape the page.")

api.add_resource(laptops, '/laptops/<brand>')

if __name__ == "__main__":
    app.run(debug=True)

