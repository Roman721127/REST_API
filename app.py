from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo_admin:password@localhost:27017")
client = MongoClient(MONGO_URL)
db = client.library

class BookList(Resource):
    def get(self):
        """
        ---
        responses:
          200:
            description: OK
        """
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        books = list(db.books.find().skip(offset).limit(limit))
        for b in books:
            b['_id'] = str(b['_id'])
        return {"items": books, "total": db.books.count_documents({})}, 200

    def post(self):
        """
        ---
        parameters:
          - in: body
            name: body
            schema:
              properties:
                title: {type: string}
                author: {type: string}
                year: {type: integer}
                status: {type: string}
        responses:
          201:
            description: Created
        """
        data = request.get_json()
        result = db.books.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return data, 201

class BookItem(Resource):
    def get(self, book_id):
        """
        ---
        parameters:
          - in: path
            name: book_id
            type: string
            required: true
        responses:
          200:
            description: OK
        """
        book = db.books.find_one({"_id": ObjectId(book_id)})
        if book:
            book['_id'] = str(book['_id'])
            return book, 200
        return {"message": "Not found"}, 404

    def put(self, book_id):
        """
        ---
        parameters:
          - in: path
            name: book_id
            type: string
            required: true
          - in: body
            name: body
            schema:
              properties:
                title: {type: string}
                author: {type: string}
                year: {type: integer}
                status: {type: string}
        responses:
          200:
            description: Updated
        """
        data = request.get_json()
        result = db.books.update_one({"_id": ObjectId(book_id)}, {"$set": data})
        if result.matched_count:
            return {"message": "Updated"}, 200
        return {"message": "Not found"}, 404

    def delete(self, book_id):
        """
        ---
        parameters:
          - in: path
            name: book_id
            type: string
            required: true
        responses:
          204:
            description: Deleted
        """
        result = db.books.delete_one({"_id": ObjectId(book_id)})
        if result.deleted_count:
            return '', 204
        return {"message": "Not found"}, 404

api.add_resource(BookList, '/books')
api.add_resource(BookItem, '/books/<string:book_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)