from flask_restful import Resource
import helloworld.models


class PlanetRes(Resource):
    def post(self):
        return

    def get(self):
        return [{'id': planet.id,
                 'name': planet.name}
                for planet in helloworld.models.Planet.query.all()]
