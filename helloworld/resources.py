# -*- coding: utf-8 -*-
import flask
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
import helloworld.models
from helloworld.database import db


class PlanetRes(Resource):
    def post(self):
        data = flask.request.get_json()
        if not data:
            raise BadRequest("Request data must be JSON.")
        try:
            name = data['name']
        except KeyError:
            raise BadRequest("JSON body must include the `name` key.")

        planet = helloworld.models.Planet(name=name)
        db.session.add(planet)
        db.session.commit()
        return '', 202  # Accepted

    def get(self):
        return [{'id': planet.id, 'name': planet.name}
                for planet in helloworld.models.Planet.query.all()]
