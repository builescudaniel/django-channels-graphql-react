# Import the necessary modules from graphene and the schema from the 'app' module
import graphene
import app.schema

# Define a Query class that inherits from the Query class defined in app.schema and graphene's ObjectType
class Query(app.schema.Query, graphene.ObjectType):
    pass

# Define a GraphQL schema with the above Query class as its query root
schema = graphene.Schema(query=Query)