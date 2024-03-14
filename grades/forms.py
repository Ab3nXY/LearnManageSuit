from django import forms
from django.forms import modelformset_factory
from .models import Student

class ExamForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'score', 'email']
        
ExamFormSet = modelformset_factory(Student, form=ExamForm, extra=15)  # Adjust 'extra' based on your needs
