# Importing necessary modules from the Django framework
from django.contrib import admin
from django.urls import path

# Importing the GraphQLView from the Graphene-Django package, which allows us to handle GraphQL queries
from graphene_django.views import GraphQLView

# Defining the URL patterns for the Django application
urlpatterns = [
    # Linking the default Django admin interface to the URL path 'admin/'
    path('admin/', admin.site.urls),
    
    # Linking the GraphQL endpoint to the URL path 'graphql/'. The `graphiql` parameter set to True 
    # provides an interactive in-browser GraphQL IDE, useful for testing and understanding our GraphQL API.
    path('graphql/', GraphQLView.as_view(graphiql=True)),  
]