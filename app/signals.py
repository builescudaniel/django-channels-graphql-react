# Importing necessary modules for Django model signals and Graphene subscriptions
from django.db.models.signals import post_save, post_delete
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription
from .models import Task  # Importing the Task model from the current directory's models module

# A custom callback function that is triggered when a Task model instance is saved.
def task_saved(sender, instance, **kwargs):
    # Printing out a message indicating the title of the task that was saved.
    print(f"Task '{instance.title}' has been saved!")

# Connecting the custom callback function to the post_save signal for the Task model.
# This ensures the task_saved function is called whenever a Task instance is saved.
post_save.connect(task_saved, sender=Task, dispatch_uid="task_saved_custom")

# Connecting the Graphene subscription's post_save_subscription function to the post_save signal for the Task model.
# This will inform any subscribers that a Task instance has been saved.
post_save.connect(post_save_subscription, sender=Task, dispatch_uid="task_post_save")

# Connecting the Graphene subscription's post_delete_subscription function to the post_delete signal for the Task model.
# This will inform any subscribers that a Task instance has been deleted.
post_delete.connect(post_delete_subscription, sender=Task, dispatch_uid="task_post_delete")