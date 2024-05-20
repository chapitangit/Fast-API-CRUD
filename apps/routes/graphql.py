import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL

from apps.views.graphql_views import Query


# Create a Strawberry schema
schema = strawberry.Schema(query=Query)
 
graphql_app = GraphQL(schema)

