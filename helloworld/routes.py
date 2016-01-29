from collections import namedtuple
from helloworld import resources


Route = namedtuple('Route', ['resource', 'urls'])

routes = [
    Route(resources.PlanetRes, ['/api/v0/planets/'])
]
