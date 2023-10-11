# Importing the necessary models module from Django's ORM
from django.db import models

# Defining a Task model which inherits from Django's Model class
class Task(models.Model):
    # Defining a character field for the task title with a maximum length of 200 characters
    title = models.CharField(max_length=200)
    
    # Defining a boolean field to indicate if the task is completed or not; default is set to False (not completed)
    completed = models.BooleanField(default=False)

    # Overriding the default string representation method to return the title of the task
    def __str__(self):
        return self.title