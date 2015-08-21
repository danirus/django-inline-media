from django import forms
from inline_media.tests.models import ModelTest


class ModelTestForm(forms.ModelForm):
    class Meta:
        model = ModelTest
        fields = ['first_text', 'second_text']
