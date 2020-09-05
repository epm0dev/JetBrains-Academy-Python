from django.db.models import Model, CharField, ForeignKey, CASCADE
from django.contrib.auth.models import User


# A subclass of Django's Model class that represents a database table entry containing a resume.
class Resume(Model):
    # Define a character field containing a resume's description.
    description = CharField(max_length=1024)

    # Define a foreign key field containing a resume's author represented as a User object.
    author = ForeignKey(User, on_delete=CASCADE)
