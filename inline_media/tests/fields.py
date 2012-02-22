#-*- coding: utf-8 -*-

from django import forms
from django.db import models
from django.test import TestCase as DjangoTestCase

from inline_media.models import Picture
from inline_media.fields import TextFieldWithInlines
from inline_media.tests.models import ModelTest


class TextFieldWithInlinesTestCase(DjangoTestCase):

    def setUp(self):
        self.object = ModelTest.objects.create(first_text="Hello", second_text="World")

    def test_widget_for_textfieldwithinlines_model_field(self):
        class FormTest(forms.ModelForm):
            class Meta:
                model = ModelTest
            
        form = FormTest()
        first_field = form.fields.get("first_text")
        second_field = form.fields.get("second_text")
        self.assert_(first_field.widget.__class__.__name__ == "Textarea")
        self.assert_(second_field.widget.__class__.__name__ == "TextareaWithInlines")
        self.assert_(True == True)
