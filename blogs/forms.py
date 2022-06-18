from django import forms
from .models import Comment

class FormComment(forms.ModelForm):
    class Meta:
        model= Comment
        fields= ["Class", "Detail", "Department", "Aspect","words","date"]