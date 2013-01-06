#-*- coding: utf-8 -*-

from django import forms
from inline_media.tests.models import TestModel


class TestModelForm(forms.ModelForm):
    class Meta:
        model = TestModel
