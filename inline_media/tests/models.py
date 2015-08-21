from django.db import models
from inline_media.fields import TextFieldWithInlines


class ModelTest(models.Model):
    first_text = models.TextField()
    second_text = TextFieldWithInlines()


class AnotherModelTest(models.Model):
    first_text = models.TextField()
    second_text = TextFieldWithInlines()


# class whose objects may be inserted as inline elements, does not need any
# specific field, just added as an InlineType, in test_parser.py
class ModelMediaTest(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1024)
