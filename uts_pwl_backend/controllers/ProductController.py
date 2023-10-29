import json
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.request import Request

from sqlalchemy.exc import DBAPIError


from ..models import Product


@view_defaults(route_name="product")
class ProductController:
    def __init__(self, request):
        self.request: Request = request

    @view_config(request_method="POST")
    def create(self):
        try:
            try:
                name = self.request.json_body["name"]
                price = self.request.json_body["price"]
                stock = self.request.json_body["stock"]
                description = self.request.json_body["description"]

            except:
                return Response(
                    content_type="application/json",
                    charset="UTF-8",
                    status=400,
                    body=json.dumps({"error": "title or content is empty"}),
                )

            product = Product(
                name=name, price=price, stock=stock, description=description
            )
            self.request.dbsession.add(product)
            self.request.dbsession.flush()

            return Response(
                json={"message": "success"},
                status=200,
                content_type="application/json",
            )

        except DBAPIError:
            return Response(
                json={"message": "failed"},
                status=500,
                content_type="application/json",
            )

    @view_config(request_method="GET")
    def read(self):
        try:
            products = self.request.dbsession.query(Product).all()
            return Response(
                json={
                    "data": [
                        {
                            "id": product.id,
                            "name": product.name,
                            "price": product.price,
                            "stock": product.stock,
                            "description": product.description,
                        }
                        for product in products
                    ]
                },
                status=200,
                content_type="application/json",
            )
        except DBAPIError:
            return Response(
                json=json.dumps({"message": "failed"}),
                status=500,
                content_type="application/json",
            )

    @view_config(request_method="PUT")
    def update(self):
        try:
            try:
                id = self.request.json_body["id"]
                name = self.request.json_body["name"]
                price = self.request.json_body["price"]
                stock = self.request.json_body["stock"]
                description = self.request.json_body["description"]

            except:
                return Response(
                    content_type="application/json",
                    charset="UTF-8",
                    status=400,
                    body=json.dumps(
                        {"error": "id, name, price, stock or description is empty"}
                    ),
                )

            product = self.request.dbsession.query(Product).filter_by(id=id).first()

            product.name = name
            product.price = price
            product.stock = stock
            product.description = description

            self.request.dbsession.flush()

            return Response(
                json={"message": "success"},
                status=201,
                content_type="application/json",
            )
        except DBAPIError:
            return Response(
                json={"message": "failed"},
                status=500,
                content_type="application/json",
            )

    @view_config(request_method="DELETE")
    def delete(self):
        try:
            try:
                id = self.request.json_body["id"]
            except:
                return Response(
                    content_type="application/json",
                    charset="UTF-8",
                    status=400,
                    body=json.dumps({"error": "id is empty"}),
                )

            product = self.request.dbsession.query(Product).filter_by(id=id).first()
            self.request.dbsession.delete(product)
            self.request.dbsession.flush()

            return Response(
                json={"message": "success"},
                status=200,
                content_type="application/json",
            )
        except DBAPIError:
            return Response(
                json={"message": "failed"},
                status=500,
                content_type="application/json",
            )
