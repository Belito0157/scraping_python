from flask import Flask, jsonify
from flask_restful import Api, Resource
from scrapping_service import ScrappingService 

app = Flask(__name__)
api = Api(app)

class laptops(Resource):
    def get(self, brand):
        scrapping_service = ScrappingService()
        laptops = scrapping_service.scrape_all_laptops(brand)
        return jsonify(laptops)

api.add_resource(laptops, '/laptops/<brand>')

if __name__ == "__main__":
    app.run(debug=True)

