from app import api
from flask_restful import Resource


class Hello(Resource):
    def get(self):
        return {'hello': 'hello'}


api.add_resource(Hello, '/api/hello')
