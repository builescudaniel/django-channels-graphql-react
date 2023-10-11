# Import the necessary modules from graphene, graphene_django, and the local models
import graphene
from graphene_django.types import DjangoObjectType
from .models import Task
from graphene_subscriptions.events import CREATED, DELETED

# Define the TaskType which is a representation of the Task model in GraphQL
class TaskType(DjangoObjectType):
    class Meta:
        model = Task

# Subscription for when a task is created
class TaskCreatedSubscription(graphene.ObjectType):
    task_created = graphene.Field(TaskType)

    def resolve_task_created(root, info):
        return root.filter(
            lambda event: 
                event.operation == CREATED and
                isinstance(event.instance, Task)
        ).map(lambda event: event.instance)

# Subscription for when a task is deleted
class TaskDeletedSubscription(graphene.ObjectType):
    task_deleted = graphene.Field(TaskType)

    def resolve_task_deleted(root, info):
        return root.filter(
            lambda event: 
                event.operation == DELETED and
                isinstance(event.instance, Task)
        ).map(lambda event: event.instance)

# GraphQL query to fetch all tasks
class Query(graphene.ObjectType):
    all_tasks = graphene.List(TaskType)

    def resolve_all_tasks(self, info, **kwargs):
        return Task.objects.all()

# GraphQL mutation to create a task
class CreateTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        title = graphene.String(required=True)
        completed = graphene.Boolean(required=True)

    @staticmethod
    def mutate(root, info, title, completed):
        task = Task(title=title, completed=completed)
        task.save()
        return CreateTask(task=task)

# GraphQL mutation to delete a task
class DeleteTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        id = graphene.ID(required=True)

    @staticmethod
    def mutate(root, info, id):
        task = Task.objects.get(pk=id)
        task_instance = Task(title=task.title, completed=task.completed)
        task.delete()
        return DeleteTask(task=task_instance)

# Aggregating all mutations
class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    delete_task = DeleteTask.Field()

# Aggregating all subscriptions
class Subscription(TaskCreatedSubscription, TaskDeletedSubscription, graphene.ObjectType):
    pass

# Creating the overall schema for GraphQL
schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)